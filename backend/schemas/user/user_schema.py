from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
from schemas.profile.profile_schema import ProfileBase


class UserBase(BaseModel):

    username: str
    email: str
    password: str
    # isAdmin: bool = False
    # profile_Image: str = "http://res.cloudinary.com/dxvfbzh7b/image/upload/c_limit,h_800,w_800/q_auto/f_auto/v1/Books_Project/hjb5hdz4mhifey25qgmu"

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None

    password: Optional[str] = None
    profile: Optional[ProfileBase] = None


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):

    username: str
    email: str
    isAdmin: bool = False
    profile_Image: str

    class Config:
        from_attributes = True
