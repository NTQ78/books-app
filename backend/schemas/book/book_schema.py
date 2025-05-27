from pydantic import BaseModel, Field, validator
from pydantic.config import ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import Form, File, UploadFile


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Title cannot be empty")
    author: str = Field(..., min_length=1, description="Author cannot be empty")
    caption: str = Field(..., min_length=1, description="Caption cannot be empty")
    summary: str = Field(..., min_length=1, description="Summary cannot be empty")

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    pass

    @classmethod
    def as_form(
        cls,
        title: str = Form(..., min_length=1),
        author: str = Form(..., min_length=1),
        caption: str = Form(..., min_length=1),
        summary: str = Form(..., min_length=1),
    ):
        return cls(
            title=title,
            author=author,
            caption=caption,
            summary=summary,
        )


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    title: str
    author: str
    caption: str
    summary: str
    cover_image: str
    user_id: str
    create_At: datetime

    model_config = ConfigDict(from_attributes=True)
