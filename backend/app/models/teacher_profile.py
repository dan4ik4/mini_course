from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class TeacherProfile(Base):
    __tablename__ = "teacher_profile"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    user = relationship(
    "User",
    back_populates="teacher_profile",
    passive_deletes=True,
)

    specialization = Column(String(255))
    experience_years = Column(Integer)
    bio = Column(Text)