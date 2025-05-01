from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from database.mysql import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Profile(Base):
    __tablename__ = "Profile"
    profile_id = Column(
        String(255),
        ForeignKey("Users.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        unique=True,
    )
    isAdmin = Column(Boolean, default=False)
    profile_Image = Column(String(255))
    isAuthor = Column(Boolean, default=False)
    create_At = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="profile", uselist=False)

    def to_dict(self):
        return {
            "username": self.user.username if self.user else None,
            "email": self.user.email if self.user else None,
            "isAdmin": self.isAdmin,
            "isAuthor": self.isAuthor,
            "profile_Image": self.profile_Image,
            "create_At": self.create_At.strftime("%Y-%m-%d %H:%M:%S"),
        }
