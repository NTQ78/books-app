from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import Form, File, UploadFile


class BookBase(BaseModel):
    title: str
    author: str
    caption: str
    summary: str

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    pass

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        author: str = Form(...),
        caption: str = Form(...),
        summary: str = Form(...),
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
