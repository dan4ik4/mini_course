import uuid
from sqlalchemy import String, Boolean, TIMESTAMP, func, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.db.base import Base

import enum

from datetime import datetime

from sqlalchemy.orm import relationship


profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserRole(str, enum.Enum):
    user = "user"
    teacher = "teacher"
    owner = "owner"


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.user, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    teacher_profile = relationship(
    "TeacherProfile",
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan",
    passive_deletes=True,
)