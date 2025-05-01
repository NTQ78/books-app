from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship

from database.mysql import Base
import uuid


class Book(Base):
    __tablename__ = "Books"

    id = Column(
        String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    title = Column(String(255), unique=False, index=True, nullable=False)
    author = Column(String(255), nullable=False)
    caption = Column(String(255))
    summary = Column(String(255))
    cover_image = Column(String(255))
    user_id = Column(
        String(255), ForeignKey("Users.id", onupdate="CASCADE"), nullable=False
    )
    create_At = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="books")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "caption": self.caption,
            "summary": self.summary,
            "cover_image": self.cover_image,
            "user_id": self.user_id,
            "create_At": self.create_At.strftime("%Y-%m-%d %H:%M:%S"),
        }
