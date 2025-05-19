from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from schemas.profile.profile_schema import ProfileBase


class UserBase(BaseModel):

    username: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    profile: Optional[ProfileBase] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):

    username: str
    email: str
    isAdmin: bool = False
    profile_Image: str

    model_config = ConfigDict(from_attributes=True)
