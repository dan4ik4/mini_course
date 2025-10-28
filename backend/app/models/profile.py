from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    display_name = Column(String(120))
    bio = Column(Text)
    timezone = Column(String(64))
    avatar_url = Column(String(512))
    phone = Column(String(32))
    telegram = Column(String(64))
    birth_date = Column(Date)

    user = relationship("User", back_populates="profile", uselist=False)
