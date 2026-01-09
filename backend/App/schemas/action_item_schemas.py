from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from App.models.model import ActionStatus
from App.schemas.user_schema import UserRead

class ConfigBase:
    form_attribute = True

class ActionItemBase(BaseModel):
    task: str = Field(..., examples=["Review final slide deck for client meeting"])
    assignee_id: Optional[int] = Field(None, examples=[2], description="ID of the user assigned the task.")
    due_date: Optional[datetime] = None

class ActionItemCreate(ActionItemBase):
    status: ActionStatus
    class Config(ConfigBase):
        pass

class ActionItemRead(ActionItemBase):
    id: int
    meeting_id: int
    status: ActionStatus
    due_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ActionItemDisplay(BaseModel):
    id: int
    task: str
    assignee: UserRead
    due_date: datetime
    status: ActionStatus

    class Config:
        from_attributes = True

class ActionItemDisplayList(BaseModel):
    action_items: list[ActionItemDisplay]


class ActionItemResponse(BaseModel):
    message: str
    action_item: ActionItemRead