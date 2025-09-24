from __future__ import annotations
from enum import StrEnum
from sqlalchemy import String, Enum as SAEnum, Boolean, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class Role(StrEnum):
    USER = "user"
    PSYCHOLOGIST = "psychologist"
    OWNER = "owner"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(
        SAEnum(Role, name="role_enum", native_enum=False),
        default=Role.USER,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
