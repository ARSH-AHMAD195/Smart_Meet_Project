from fastapi import Depends
from sqlalchemy.orm import Session
from App.models.model import ActionItem, Meeting, Team
from App.services.ai_service import GeminiLLM
from App.core.database import get_db
from datetime import datetime
from typing import List, Dict

DBSession = Depends(get_db)

class AgendaService:
    def __init__(self, llm: GeminiLLM) -> None:
        self.llm = llm


    def get_unresolved_action_items(self, team_id: int, db: Session = DBSession) -> List[ActionItem]:
        return (
            db.query(ActionItem).join(Meeting).filter(Meeting.team_id == team_id, ActionItem.status != "COMPLETED").all()
        )
    
    def suggest_next_agenda(self, team_id: int, db: Session = DBSession) -> Dict:
        
        team = db.get(Team, team_id)
        if not team:
            return {
                "ERROR":"TEAM NOT FOUND"
            }
        
        unresolved = (
            db.query(ActionItem)
              .join(Meeting)
              .filter(Meeting.team_id == team_id, ActionItem.status != "COMPLETED")
              .all()
        )

        if not unresolved:
            if bool(team.project_description or ""):
                prompt = f"""
                Generate a first meeting agenda for the {team.name} team.
                Context: {team.project_description}.
                The meeting should cover introductions, objectives, and planning next steps.
                Provide 5 concise bullet points.

                Make sure that all the above points are in non-bold form.
                """
                agenda_text = self.llm.generate(prompt, max_tokens=256, temperature=0.0)

                return {
                    "team_id": team_id,
                    "type": "AI-Kickoff",
                    "suggested_agenda": [a.strip("-• ") for a in agenda_text.split("\n") if a.strip()],
                    "pending_actions": [],
                }
            
            return {
                "team_id": team_id,
                "type": "Default Kickoff",
                "suggested_agenda": [
                    "Welcome and team introductions",
                    "Define project goals and scope",
                    "Outline key milestones",
                    "Assign initial responsibilities",
                    "Decide communication & meeting cadence",
                ],
                "pending_actions": [],
            }
        
        suggestions = []
        print(unresolved)
        print(type(unresolved))
        for item in unresolved:
            suggestions.append({
                "task": item.task,
                "assignee": item.assignee,
                "due_date": item.due_date,
                "status": item.status
            })
        
        return {
            "team_id": team_id,
            "suggested_agenda": [
                "Review unresolved action items",
                "Plan next deliverables",
                "Address blockers or delays",
                "Set priorities for next sprint"
            ],
            "pending_actions": suggestions
        }