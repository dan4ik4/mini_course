import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, Text, Date, Integer
from sqlalchemy.orm import relationship

from app.core.db import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    display_name = Column(String(120))
    bio = Column(Text)
    timezone = Column(String(64))
    avatar_url = Column(String(512))
    phone = Column(String(32))
    telegram = Column(String(64))
    birth_date = Column(Date)

    user = relationship("User", back_populates="profile", uselist=False)
