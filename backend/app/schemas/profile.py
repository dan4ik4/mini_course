from typing import Optional
from datetime import date
from pydantic import BaseModel, HttpUrl, Field


class ProfileBase(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, strip_whitespace=True)
    bio: Optional[str] = None
    timezone: Optional[str] = Field(None, min_length=1, strip_whitespace=True)
    avatar_url: Optional[HttpUrl] = None
    phone: Optional[str] = Field(None, min_length=3, max_length=32, strip_whitespace=True)
    telegram: Optional[str] = Field(None, min_length=2, max_length=64, strip_whitespace=True)
    birth_date: Optional[date] = None


class ProfileUpdate(ProfileBase):
    """Данные для PATCH /profile/me"""
    pass


class ProfileOut(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
