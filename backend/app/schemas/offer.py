from pydantic import BaseModel
from app.schemas.lesson import LessonOut
from uuid import UUID

class OfferCreate(BaseModel):
    subject_id: int

class OfferOut(BaseModel):
    id: int
    subject_id: int
    teacher_id: UUID

    class Config:
        from_attributes = True

class OfferDetailOut(BaseModel):
    id: int
    subject_id: int
    teacher_id: UUID
    lessons: list[LessonOut] = []

    class Config:
        from_attributes = True