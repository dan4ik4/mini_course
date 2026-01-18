import enum

class LessonKind(str, enum.Enum):
    lecture = "lecture"
    practice = "practice"