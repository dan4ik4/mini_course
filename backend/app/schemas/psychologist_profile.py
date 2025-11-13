from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class PsychologistProfileBase(BaseModel):
    specialization: Optional[str] = Field(None, max_length=255)
    experience_years: Optional[int] = None
    license_number: Optional[str] = Field(None, max_length=255)
    price_per_hour: Optional[int] = None
    bio: Optional[str] = None


class PsychologistProfileUpdate(PsychologistProfileBase):
    #specialization: Optional[str] = None
    experience_years: Optional[int] = None
    #license_number: Optional[str] = None
    price_per_hour: Optional[int] = None
    bio: Optional[str] = None
    #pass


class PsychologistProfileOut(PsychologistProfileBase):
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    license_number: Optional[str] = None
    price_per_hour: Optional[int] = None
    bio: Optional[str] = None
    id: int
    user_id: UUID  # UUID как строка
