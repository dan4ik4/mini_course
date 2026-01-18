from pydantic import BaseModel
from datetime import time
from app.models.enums import LessonKind

class LessonCreate(BaseModel):
    kind: LessonKind
    weekday: int
    start_time: time
    end_time: time
    capacity: int

class LessonOut(LessonCreate):
    id: int

    class Config:
        from_attributes = True
