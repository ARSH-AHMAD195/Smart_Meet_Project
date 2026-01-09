from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ConfigBase:
    form_attribute = True

class UserBase(BaseModel):
    username: str = Field(..., examples=["Alice Smith"])
    email: str = Field(..., examples=["alice@team.com"])

class UserCreate(UserBase):
    password: str 

class UserRead(UserBase):
    class Config(ConfigBase):
        pass
