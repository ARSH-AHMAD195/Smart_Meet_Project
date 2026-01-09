from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from App.services.ai_service import GeminiLLM, GeminiEmbedding, InMemoryVectorStore, RAGService
from App.core.database import get_db
from App.core.utils import parse_due_date_natural
from sqlalchemy.orm import Session, joinedload
from App.schemas.meet_schemas import MeetingRead
from App.schemas.ai_schemas import AgendaOutputSchema, ExtractedActionItem
from App.schemas.summary_schemas import SummaryRead
from App.schemas.action_item_schemas import ActionItemResponse, ActionItemDisplayList, ActionItemCreate
from App.models.model import User, Team, Meeting, Transcript, ActionItem, ActionStatus, MeetSummary
from typing import Annotated
from datetime import datetime
import logging


router = APIRouter()
DbSession = Depends(get_db)

# Initializing the AI service
llm = GeminiLLM()
embedder = GeminiEmbedding()
store = InMemoryVectorStore()
rag_service = RAGService(llm=llm, embedder=embedder, vectorstore=store)

logger = logging.getLogger("meetings_router")
logger.setLevel(logging.INFO)


@router.post("/", response_model=MeetingRead, status_code=status.HTTP_201_CREATED)
async def create_meeting_and_upload_transcript(
    team_id: Annotated[int, Form()], 
    topic: Annotated[str, Form()],
    transcript_file: Annotated[UploadFile, File()],
    db: Session = DbSession,
):
    """Creates a new Meeting and uploads the raw transcript text."""
    
    try:
        raw_text_bytes = await transcript_file.read()
        raw_text = raw_text_bytes.decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")
    
    # Check if the team exists
    if not db.get(Team, team_id):
        raise HTTPException(status_code=404, detail="Team not found")

    # 1. Create the Meeting record
    new_meeting = Meeting(team_id=team_id, topic=topic)
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    # 2. Create the Transcript record, linking to the meeting
    new_transcript = Transcript(meeting_id=new_meeting.id, raw_text=raw_text)
    db.add(new_transcript)
    db.commit()

    # The returned meeting object includes the relationships defined in models/meeting.py
    return new_meeting


@router.post("/{meeting_id}/generate_meeting_summary", response_model=AgendaOutputSchema)
def generate_meeting_summary_and_action_items(meeting_id: int, db: Session = DbSession):
    """Generate structured summary and action items for a meeting."""
    
    # 1️⃣ Fetch the meeting and transcript
    db_meeting = db.get(Meeting, meeting_id)
    if not db_meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    transcript = db.query(Transcript).filter(Transcript.meeting_id == meeting_id).first()
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found for this meeting")

    # 2️⃣ Call the AI service to index + summarize
    transcript_id = f"meeting_{meeting_id}"
    rag_service.index_transcript(transcript_id, str(transcript.raw_text), metadata={"meeting_topic": db_meeting.topic})
    
    result = rag_service.summarize_transcript(transcript_id)

    # 3️⃣ Parse and save the action items into DB
    created_actions = []
    for ai in result.action_items:
        due_date_parsed = parse_due_date_natural(ai.due_date)
        assignee_id = None

        # Try to resolve assignee by name (if exists in DB)
        if ai.assignee and ai.assignee.lower() != "unassigned":
            user = db.query(User).filter(User.username.ilike(f"%{ai.assignee}%")).first()
            assignee_id = user.id if user else None

        existing = db.query(ActionItem).filter(
            ActionItem.meeting_id == meeting_id,
            ActionItem.task == ai.description,
            ActionItem.assignee_id == assignee_id
        ).first()

        if existing:
            created_actions.append(existing)
            continue  # skip creating duplicate

        action = ActionItem(
            meeting_id=meeting_id,
            task=ai.description,
            assignee_id=assignee_id,
            due_date=due_date_parsed,
            status="PENDING"
        )

        db.add(action)
        created_actions.append(action)

    db.commit()

    summary_input = result.summary
    parts = [p.strip() for p in summary_input.split("HIGHLIGHTS:")]
    executive = parts[0].replace("\n", " ").strip()
    executive_summary = executive.replace("EXECUTIVE SUMMARY:","").strip()
    highlight = parts[1].replace("- ","").strip().split("\n") if len(parts) > 1 else []
    
    highlights = ""
    for idx, h in enumerate(highlight):
        highlights+=(f"{idx+1}.{h} ")
    
    summary_output = [{"EXECUTIVE SUMMARY":executive_summary},{"HIGHLIGHTS":highlights}]

    existing_summary = db.query(MeetSummary).filter(MeetSummary.meeting_id == meeting_id, MeetSummary.summary == executive_summary).first()
    if not existing_summary:
        summary = MeetSummary(
            meeting_id=meeting_id,
            summary=executive_summary,
            date=datetime.now()
        )

        db.add(summary)
        db.commit()

    # 4️⃣ Return structured result
    structured_output = AgendaOutputSchema(
        summary=summary_output,
        action_items=[
            ExtractedActionItem(
                task=ai.description,
                assignee_name=ai.assignee or "Unassigned",
                status=ActionStatus.PENDING
            )
            for ai in result.action_items
        ]
    )

    return structured_output

@router.post("/{meeting_id}/add_action_item", response_model=ActionItemResponse)
def add_action_item(meeting_id: int, action_item: ActionItemCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(ActionItem).filter(
            ActionItem.meeting_id == meeting_id,
            ActionItem.task == action_item.task,
            ActionItem.assignee_id == action_item.assignee_id
        ).first()

        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Action Item already exists.")  # skip creating duplicate

        new_action_item = ActionItem(
            meeting_id=meeting_id,
            task=action_item.task,
            assignee_id=action_item.assignee_id,
            due_date=action_item.due_date,
            status="PENDING"
        )
        
        db.add(new_action_item)
        db.commit()
        db.refresh(new_action_item)

        return {
            "message" : "Action item added successfully",
            "action_item": new_action_item
        }
    except HTTPException as e:
        raise e
    
    


@router.get("/{meeting_id}", response_model=MeetingRead)
def read_meeting_details(meeting_id: int, db: Session = DbSession):
    """Retrieve meeting details, including linked action items (if any)."""
    db_meeting = db.get(Meeting, meeting_id)
    if db_meeting is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    # This automatically loads action_items if they exist, thanks to the ORM model relationship
    return db_meeting

@router.get("/{meeting_id}/summary", response_model=SummaryRead)
def read_meeting_summary(meeting_id: int, db: Session = Depends(get_db)):
    meet_summary = (
        db.query(MeetSummary)
        .options(
            joinedload(MeetSummary.meeting)
            .joinedload(Meeting.team)
        )
        .filter(MeetSummary.meeting_id == meeting_id)
        .first()
    )

    if not meet_summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )

    return {
        "summary": meet_summary.summary,
        "date": meet_summary.date,
        "meet_details": {
            "topic": meet_summary.meeting.topic
        }
    }

@router.get("/{meeting_id}/action-items", response_model=ActionItemDisplayList)
def read_action_items(meeting_id: int, db: Session = Depends(get_db)):
    meet_action_items = db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).all()
    if meet_action_items is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action Items not found")
    
    return {"action_items":meet_action_items}

# Future feature for Live Meet Caption Captured Transcript
# ========================================================

# @router.get("/{meeting_id}/transcript", response_model=TranscriptRead)
# def read_raw_transcript(meeting_id: int, db: Session = DbSession):
#     """Retrieve the raw text content of the transcript for a meeting."""
#     db_transcript = db.query(Transcript).filter(
#         Transcript.meeting_id == meeting_id
#     ).first()
    
#     if db_transcript is None:
#         raise HTTPException(status_code=404, detail="Transcript not found for this meeting")
        
#     return db_transcript


@router.put("/action-item/{action_id}")
def update_action_item(action_id: int, update_status: str, db: Session = Depends(get_db)):
    action = db.get(ActionItem, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action item not found")

    if update_status.lower() == "inprogress":
        action.status = ActionStatus.INPROGRESS # type: ignore
    if update_status.lower() == "complete":
        action.status = ActionStatus.COMPLETE # type: ignore
    if update_status.lower() == "cancelled":
        action.status = ActionStatus.CANCELLED # type: ignore
    
    db.commit()
    db.refresh(action)
    return {
        "message": "Action item updated successfully",
        "action_item": {
            "id": action.id,
            "task": action.task,
            "due_date": action.due_date,
            "status": action.status
        }
    }