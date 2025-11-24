from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.deps import get_async_session, require_role
from app.models.user import User, UserRole
from app.models.psychologist_profile import PsychologistProfile
from app.schemas.psychologist_profile import (
    PsychologistProfileOut,
    PsychologistProfileUpdate,
)

router = APIRouter(
    prefix="/psychologist",
    tags=["psychologist"],
)


# получить свой психо-профиль
@router.get("/me", response_model=PsychologistProfileOut)
async def get_my_psychologist_profile(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(require_role(UserRole.psychologist)),
):
    result = await session.execute(
        select(PsychologistProfile).where(PsychologistProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()

    # если нет — создаём пустой профиль
    if profile is None:
        profile = PsychologistProfile(user_id=user.id)
        session.add(profile)
        await session.commit()
        await session.refresh(profile)

    return profile


# обновить свой психо-профиль
@router.patch("/me", response_model=PsychologistProfileUpdate)#возможно надо будет вернуть out
async def update_my_psychologist_profile(
    data: PsychologistProfileUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(require_role(UserRole.psychologist)),
):
    result = await session.execute(
        select(PsychologistProfile).where(PsychologistProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()

    if profile is None:
        profile = PsychologistProfile(user_id=user.id)
        session.add(profile)

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    await session.commit()
    await session.refresh(profile)

    return profile
