from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class TeacherProfileBase(BaseModel):
    specialization: Optional[str] = Field(None, max_length=255)
    experience_years: Optional[int] = None
    license_number: Optional[str] = Field(None, max_length=255)
    price_per_hour: Optional[int] = None
    bio: Optional[str] = None


class TeacherProfileUpdate(TeacherProfileBase):
    pass


class TeacherProfileOut(TeacherProfileBase):
    id: UUID
    user_id: UUID
