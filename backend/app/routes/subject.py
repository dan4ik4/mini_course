from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectOut
from app.auth.permissions import require_owner  # твой deps
from app.schemas.offer import OfferOut
from app.models.offer import Offer

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.get("/", response_model=list[SubjectOut])
async def list_subjects(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Subject).order_by(Subject.name))
    return res.scalars().all()

@router.post("/", response_model=SubjectOut, dependencies=[Depends(require_owner)])
async def create_subject(payload: SubjectCreate, db: AsyncSession = Depends(get_db)):
    subject = Subject(name=payload.name)
    db.add(subject)
    await db.commit()
    await db.refresh(subject)
    return subject

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_owner)])
async def delete_subject(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        delete(Subject).where(Subject.id == subject_id)
    )
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    await db.commit()

@router.get("/{subject_id}/offers", response_model=list[OfferOut])
async def list_offers_for_subject(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(
        select(Offer)
        .where(Offer.subject_id == subject_id)
        .options(selectinload(Offer.lessons))
        .order_by(Offer.id)
    )
    return res.scalars().all()