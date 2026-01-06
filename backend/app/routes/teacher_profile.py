from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.deps import get_async_session
from app.models.user import User, UserRole
from backend.app.models.teacher_profile import TeacherProfile
from app.schemas.teacher_profile import (
    TeacherProfileOut,
    TeacherProfileUpdate,
)
from app.auth.permissions import require_teacher

router = APIRouter(
    prefix="/teacher",
    tags=["teacher"],
)


# получить свой психо-профиль
@router.get("/me", response_model=TeacherProfileOut)
async def get_my_teacher_profile(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(require_teacher),
):
    result = await session.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()

    # если нет — создаём пустой профиль
    if profile is None:
        profile = TeacherProfile(user_id=user.id)
        session.add(profile)
        await session.commit()
        await session.refresh(profile)

    return profile


# обновить свой психо-профиль
@router.patch("/me", response_model=TeacherProfileUpdate)#возможно надо будет вернуть out
async def update_my_teacher_profile(
    data: TeacherProfileUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(require_teacher),
):
    result = await session.execute(
        select(TeacherProfile).where(TeacherProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()

    if profile is None:
        profile = TeacherProfile(user_id=user.id)
        session.add(profile)

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    await session.commit()
    await session.refresh(profile)

    return profile
