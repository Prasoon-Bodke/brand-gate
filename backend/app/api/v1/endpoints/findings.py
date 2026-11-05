from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.brand import Finding
from app.schemas.brand import FindingCreate, FindingUpdate, FindingResponse

router = APIRouter()


@router.get("", response_model=List[FindingResponse])
async def list_findings(
    skip: int = 0,
    limit: int = 100,
    submission_id: UUID = None,
    tier: int = None,
    status_filter: str = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Finding)
    if submission_id:
        query = query.where(Finding.content_submission_id == submission_id)
    if tier is not None:
        query = query.where(Finding.tier == tier)
    if status_filter:
        query = query.where(Finding.status == status_filter)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    findings = result.scalars().all()
    return findings


@router.post("", response_model=FindingResponse, status_code=status.HTTP_201_CREATED)
async def create_finding(
    finding_in: FindingCreate,
    db: AsyncSession = Depends(get_db),
):
    finding = Finding(**finding_in.model_dump())
    db.add(finding)
    await db.commit()
    await db.refresh(finding)
    return finding


@router.get("/{finding_id}", response_model=FindingResponse)
async def get_finding(
    finding_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Finding).where(Finding.id == finding_id))
    finding = result.scalar_one_or_none()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding


@router.patch("/{finding_id}", response_model=FindingResponse)
async def update_finding(
    finding_id: UUID,
    finding_update: FindingUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Finding).where(Finding.id == finding_id))
    finding = result.scalar_one_or_none()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")

    update_data = finding_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(finding, field, value)

    await db.commit()
    await db.refresh(finding)
    return finding


@router.delete("/{finding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_finding(
    finding_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Finding).where(Finding.id == finding_id))
    finding = result.scalar_one_or_none()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")

    await db.delete(finding)
    await db.commit()