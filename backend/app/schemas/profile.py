from typing import Optional
from datetime import date
from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from uuid import UUID


class ProfileBase(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, strip_whitespace=True)
    bio: Optional[str] = None
    timezone: Optional[str] = Field(None, min_length=1, strip_whitespace=True)
    avatar_url: Optional[HttpUrl] = None
    phone: Optional[str] = Field(None, min_length=3, max_length=32, strip_whitespace=True)
    telegram: Optional[str] = Field(None, min_length=2, max_length=64, strip_whitespace=True)
    birth_date: Optional[date] = None


class ProfileUpdate(ProfileBase):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    telegram: Optional[str] = None
    birth_date: Optional[date] = None
    #pass


class ProfileOut(BaseModel):
    id: int
    user_id: UUID
    display_name: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    telegram: Optional[str] = None
    birth_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)