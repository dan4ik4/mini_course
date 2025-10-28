from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.schemas.profile import ProfileUpdate


def get_by_user_id(db: Session, user_id: int) -> Profile | None:
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def create_for_user(db: Session, user_id: int) -> Profile:
    profile = Profile(user_id=user_id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def ensure_for_user(db: Session, user_id: int) -> Profile:
    prof = get_by_user_id(db, user_id)
    return prof if prof else create_for_user(db, user_id)


def update_for_user(db: Session, user_id: int, data: ProfileUpdate) -> Profile:
    prof = ensure_for_user(db, user_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(prof, field, value)
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof
