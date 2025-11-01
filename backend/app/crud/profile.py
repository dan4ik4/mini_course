from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.profile import Profile
from app.schemas.profile import ProfileUpdate


def get_by_user_id(db: Session, user_id: UUID) -> Profile | None:
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def create_for_user(db: Session, user_id: UUID) -> Profile:
    profile = Profile(user_id=user_id)
    db.add(profile)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # если вдруг параллельно уже создали — просто вернём существующий
        existing = get_by_user_id(db, user_id)
        if existing:
            return existing
        raise
    db.refresh(profile)
    return profile


def ensure_for_user(db: Session, user_id: UUID) -> Profile:
    prof = get_by_user_id(db, user_id)
    return prof if prof else create_for_user(db, user_id)


#def update_for_user(db: Session, user_id: UUID, data: ProfileUpdate) -> Profile:
#    prof = ensure_for_user(db, user_id)
#
#    for field, value in data.model_dump(exclude_unset=True).items():
#        setattr(prof, field, value)
#
#    db.add(prof)
#    db.commit()
#    db.refresh(prof)
#    return prof

def update_for_user(db: Session, user_id: UUID, data: ProfileUpdate) -> Profile:
    try:
        prof = ensure_for_user(db, user_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(prof, field, value)
        db.add(prof)
        db.commit()
        db.refresh(prof)
        return prof
    except Exception as e:
        # Чтобы не было «тихих» 500 — отдадим подробность и попадём в лог мидлвари
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"profile_update_error: {e!r}")
