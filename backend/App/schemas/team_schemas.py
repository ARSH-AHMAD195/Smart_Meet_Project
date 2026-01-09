from pydantic import BaseModel, Field

class ConfigBase:
    form_attribute = True

class TeamBase(BaseModel):
    name: str = Field(..., examples=["Project Alpha Team"])
    project_description: str = Field(..., examples=["Description of Project"])

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: int
    class Config(ConfigBase):
        pass