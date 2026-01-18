from sqlalchemy import ForeignKey, Integer, Time, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import LessonKind

class Lesson(Base):
    __tablename__ = "lessons"
    __table_args__ = (
        UniqueConstraint("offer_id", "kind", name="uq_lesson_offer_kind"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    offer_id: Mapped[int] = mapped_column(
        ForeignKey("offers.id", ondelete="CASCADE"),
        nullable=False,
    )

    kind: Mapped[LessonKind] = mapped_column(
        Enum(LessonKind, name="lesson_kind_enum"),
        nullable=False,
    )

    weekday: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..7 (пн..вс)
    start_time: Mapped[str] = mapped_column(Time, nullable=False)
    end_time: Mapped[str] = mapped_column(Time, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    offer = relationship("Offer", back_populates="lessons")
