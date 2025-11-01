from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.profile import ProfileOut, ProfileUpdate
from app.crud.profile import ensure_for_user, update_for_user

# подстрой этот импорт, если у тебя get_db в другом месте
from app.core.db import get_db

# подстрой этот импорт, если у тебя зависимость лежит в другом модуле
from app.auth.deps import current_active_user as get_current_user

from app.models.profile import Profile


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=ProfileOut)
def read_my_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ensure_for_user(db, current_user.id)


@router.patch("/me", response_model=ProfileOut)
def patch_my_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_for_user(db, current_user.id, payload)

@router.get("/__debug")
def profile_debug(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    uid = current_user.id
    count = db.query(Profile).filter(Profile.user_id == uid).count()
    return {
        "user_id": str(uid),
        "user_id_type": str(type(uid)),
        "profiles_by_user_id": count,
    }
