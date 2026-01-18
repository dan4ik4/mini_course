from uuid import UUID
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db.base import Base

class Offer(Base):
    __tablename__ = "offers"
    __table_args__ = (
        UniqueConstraint("subject_id", "teacher_id", name="uq_offer_subject_teacher"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
    )

    teacher_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    lessons = relationship("Lesson", back_populates="offer", cascade="all, delete-orphan")
