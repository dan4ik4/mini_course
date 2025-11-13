import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class PsychologistProfile(Base):
    __tablename__ = "psychologist_profiles"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # связь с User — как в Profile
    user = relationship("User", back_populates="psychologist_profile", uselist=False)

    # поля психолога — под себя подправишь
    specialization = Column(String(255))
    experience_years = Column(Integer)
    license_number = Column(String(255))
    price_per_hour = Column(Integer)
    bio = Column(Text)