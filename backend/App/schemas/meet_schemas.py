from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from App.schemas.action_item_schemas import ActionItemRead

class ConfigBase:
    form_attribute = True
    
class MeetingBase(BaseModel):
    team_id: int = Field(..., examples=[1], description="ID of the associated team.")
    topic: str = Field(..., examples=["Sprint Planning and Q4 Review"])
    
class MeetingCreate(MeetingBase):
    pass

class MeetingRead(MeetingBase):
    id: int
    date: datetime
    # Nested ActionItems allow the client to see all associated tasks
    action_items: List[ActionItemRead] = []
    
    class Config(ConfigBase):
        pass

class MeetingDetail(BaseModel):
    topic: str = Field(..., examples=["Sprint Planning and Q4 Review"])
    class Config(ConfigBase):
        pass