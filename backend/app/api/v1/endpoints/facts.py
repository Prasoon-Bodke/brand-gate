from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.brand import ApprovedFact
from app.schemas.brand import ApprovedFactCreate, ApprovedFactUpdate, ApprovedFactResponse

router = APIRouter()


@router.get("", response_model=List[ApprovedFactResponse])
async def list_facts(
    skip: int = 0,
    limit: int = 100,
    fact_type: str = None,
    is_active: bool = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(ApprovedFact)
    if fact_type:
        query = query.where(ApprovedFact.fact_type == fact_type)
    if is_active is not None:
        query = query.where(ApprovedFact.is_active == is_active)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    facts = result.scalars().all()
    return facts


@router.post("", response_model=ApprovedFactResponse, status_code=status.HTTP_201_CREATED)
async def create_fact(
    fact_in: ApprovedFactCreate,
    db: AsyncSession = Depends(get_db),
):
    fact = ApprovedFact(**fact_in.model_dump())
    db.add(fact)
    await db.commit()
    await db.refresh(fact)
    return fact


@router.get("/{fact_id}", response_model=ApprovedFactResponse)
async def get_fact(
    fact_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ApprovedFact).where(ApprovedFact.id == fact_id))
    fact = result.scalar_one_or_none()
    if not fact:
        raise HTTPException(status_code=404, detail="Fact not found")
    return fact


@router.patch("/{fact_id}", response_model=ApprovedFactResponse)
async def update_fact(
    fact_id: UUID,
    fact_update: ApprovedFactUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ApprovedFact).where(ApprovedFact.id == fact_id))
    fact = result.scalar_one_or_none()
    if not fact:
        raise HTTPException(status_code=404, detail="Fact not found")

    update_data = fact_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fact, field, value)

    await db.commit()
    await db.refresh(fact)
    return fact


@router.delete("/{fact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fact(
    fact_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ApprovedFact).where(ApprovedFact.id == fact_id))
    fact = result.scalar_one_or_none()
    if not fact:
        raise HTTPException(status_code=404, detail="Fact not found")

    await db.delete(fact)
    await db.commit()