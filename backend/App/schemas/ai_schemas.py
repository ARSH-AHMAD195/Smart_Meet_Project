from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional

from App.models.model import ActionStatus

class ExtractedActionItem(BaseModel):
    """The Pydantic structure for the AI to return for a single action item."""
    task: str = Field(..., description="The clear, specific action required.")
    assignee_name: str = Field(..., description="The full name or identifier of the person responsible, as mentioned in the transcript.")
    status: ActionStatus = Field(ActionStatus.PENDING, description="Default status is PENDING.")

class AgendaOutputSchema(BaseModel):
    """The complete structured output the AI service is expected to return."""
    summary: List[Dict[str,str]] = Field(..., description="A concise summary of the key discussion points and final decisions made in the meeting.")
    action_items: List[ExtractedActionItem] = Field(..., description="A list of all explicit action items extracted from the transcript.")
    
    model_config = ConfigDict(from_attributes=True)