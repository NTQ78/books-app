from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean

from database.mysql import Base
from sqlalchemy.orm import relationship, Session
import uuid


class User(Base):
    __tablename__ = "Users"
    id = Column(
        String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    profile = relationship("Profile", back_populates="user", uselist=False)
    books = relationship("Book", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "profile": self.profile.to_dict() if self.profile else None,
            "books": [book.to_dict() for book in self.books],
        }
