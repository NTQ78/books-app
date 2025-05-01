from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class ProfileBase(BaseModel):
    isAdmin: Optional[bool] = False
    isAuthor: Optional[bool] = False

    class Config:
        from_attributes = True
