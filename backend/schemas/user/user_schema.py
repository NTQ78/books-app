from pydantic import Field
from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from schemas.profile.profile_schema import ProfileBase


class UserBase(BaseModel):

    username: str = Field(..., min_length=1, description="Username cannot be empty")
    email: str = Field(..., min_length=1, description="Email cannot be empty")
    password: str = Field(
        ..., min_length=6, description="Password must be at least 6 characters long"
    )

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
