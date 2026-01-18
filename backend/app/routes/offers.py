from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.offer import Offer
from app.models.lesson import Lesson
from app.schemas.offer import OfferCreate, OfferOut, OfferDetailOut
from app.schemas.lesson import LessonCreate, LessonOut
from app.models.user import User, UserRole
from app.auth.deps import current_active_user
from app.auth.permissions import require_owner_or_teacher

router = APIRouter(prefix="/offers", tags=["Offers"])

@router.post("/", response_model=OfferOut, dependencies=[Depends(require_owner_or_teacher)])
async def create_offer(
    payload: OfferCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    offer = Offer(subject_id=payload.subject_id, teacher_id=user.id)
    db.add(offer)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Offer already exists for this subject/teacher")
    await db.refresh(offer)
    return offer

@router.post("/{offer_id}/lessons", response_model=LessonOut, dependencies=[Depends(require_owner_or_teacher)])
async def create_lesson_for_offer(
    offer_id: int,
    payload: LessonCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    # teacher может создавать только свои offers
    res = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = res.scalar_one_or_none()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    if user.role.name != "owner" and offer.teacher_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your offer")

    lesson = Lesson(offer_id=offer_id, **payload.model_dump())
    db.add(lesson)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Lesson of this kind already exists in offer")
    await db.refresh(lesson)
    return lesson

@router.get("/{offer_id}", response_model=OfferDetailOut)
async def get_offer(offer_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(Offer)
        .where(Offer.id == offer_id)
        .options(selectinload(Offer.lessons))
    )
    offer = res.scalar_one_or_none()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_owner_or_teacher)])
async def delete_offer(
    offer_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
):
    result = await db.execute(
        select(Offer).where(Offer.id == offer_id)
    )
    offer = result.scalar_one_or_none()

    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    if user.role != UserRole.owner and offer.teacher_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this offer",
        )

    await db.execute(delete(Offer).where(Offer.id == offer_id))
    await db.commit()