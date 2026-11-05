from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.brand import BrandGuideline
from app.schemas.brand import BrandGuidelineCreate, BrandGuidelineUpdate, BrandGuidelineResponse

router = APIRouter()


@router.get("", response_model=List[BrandGuidelineResponse])
async def list_guidelines(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    is_active: bool = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(BrandGuideline)
    if category:
        query = query.where(BrandGuideline.category == category)
    if is_active is not None:
        query = query.where(BrandGuideline.is_active == is_active)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    guidelines = result.scalars().all()
    return guidelines


@router.post("", response_model=BrandGuidelineResponse, status_code=status.HTTP_201_CREATED)
async def create_guideline(
    guideline_in: BrandGuidelineCreate,
    db: AsyncSession = Depends(get_db),
):
    guideline = BrandGuideline(**guideline_in.model_dump())
    db.add(guideline)
    await db.commit()
    await db.refresh(guideline)
    return guideline


@router.get("/{guideline_id}", response_model=BrandGuidelineResponse)
async def get_guideline(
    guideline_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(BrandGuideline).where(BrandGuideline.id == guideline_id))
    guideline = result.scalar_one_or_none()
    if not guideline:
        raise HTTPException(status_code=404, detail="Guideline not found")
    return guideline


@router.patch("/{guideline_id}", response_model=BrandGuidelineResponse)
async def update_guideline(
    guideline_id: UUID,
    guideline_update: BrandGuidelineUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(BrandGuideline).where(BrandGuideline.id == guideline_id))
    guideline = result.scalar_one_or_none()
    if not guideline:
        raise HTTPException(status_code=404, detail="Guideline not found")

    update_data = guideline_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(guideline, field, value)

    await db.commit()
    await db.refresh(guideline)
    return guideline


@router.delete("/{guideline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guideline(
    guideline_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(BrandGuideline).where(BrandGuideline.id == guideline_id))
    guideline = result.scalar_one_or_none()
    if not guideline:
        raise HTTPException(status_code=404, detail="Guideline not found")

    await db.delete(guideline)
    await db.commit()