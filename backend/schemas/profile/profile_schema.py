from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any


class ProfileBase(BaseModel):
    isAdmin: bool = False
    isAuthor: bool = False

    model_config = ConfigDict(from_attributes=True)
