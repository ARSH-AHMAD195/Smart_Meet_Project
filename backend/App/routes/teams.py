from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from App.schemas.team_schemas import TeamRead, TeamCreate
from App.models.model import Team
from App.services.ai_service import GeminiLLM
from App.services.agenda_service import AgendaService
from App.core.database import get_db


router = APIRouter()

DbSession = Depends(get_db)
llm = GeminiLLM()
agenda_service = AgendaService(llm=llm)

@router.post("/", response_model=TeamRead, status_code=201)
def create_team(team_data: TeamCreate, db: Session = DbSession):
    """Create a new team."""
    db_team = Team(**team_data.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/{team_id}", response_model=TeamRead)
def read_team(team_id: int, db: Session = DbSession):
    """Get team details by ID."""
    db_team = db.get(Team, team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.get("/{team_id}/next_agenda")
def get_next_agenda(team_id: int, db: Session = DbSession):
    """Suggest the next meeting agenda for a team."""
    result = agenda_service.suggest_next_agenda(team_id, db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result