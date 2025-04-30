from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


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
    isAdmin: Optional[bool] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):

    username: str
    email: str
    isAdmin: bool = False
    profile_Image: str = "default.jpg"

    class Config:
        from_attributes = True
