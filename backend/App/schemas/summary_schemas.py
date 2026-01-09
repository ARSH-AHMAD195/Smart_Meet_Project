from pydantic import BaseModel, Field
from datetime import datetime
from App.schemas.meet_schemas import MeetingDetail

class ConfigBase:
    form_attribute = True
    
class SummaryBase(BaseModel):
    meeting_id: int = Field(..., examples=[1], description="ID of the associated meeting.")
    summary: str = Field(..., examples=["Sprint Planning and Q4 Review..."])
    
class SummaryCreate(SummaryBase):
    pass

class SummaryRead(BaseModel):  
    meet_details: MeetingDetail
    summary: str = Field(..., examples=["Sprint Planning and Q4 Review..."])  
    date: datetime = Field(..., examples=["2025-12-16T22:32:46.558658"])  
    class Config(ConfigBase):
        pass 