from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.brand import BrandAsset
from app.schemas.brand import BrandAssetCreate, BrandAssetUpdate, BrandAssetResponse

router = APIRouter()


@router.get("", response_model=List[BrandAssetResponse])
async def list_assets(
    skip: int = 0,
    limit: int = 100,
    asset_type: str = None,
    is_active: bool = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(BrandAsset)
    if asset_type:
        query = query.where(BrandAsset.asset_type == asset_type)
    if is_active is not None:
        query = query.where(BrandAsset.is_active == is_active)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    assets = result.scalars().all()
    return assets


@router.post("", response_model=BrandAssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_in: BrandAssetCreate,
    db: AsyncSession = Depends(get_db),
):
    asset = BrandAsset(**asset_in.model_dump())
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset


@router.get("/{asset_id}", response_model=BrandAssetResponse)
async def get_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(BrandAsset).where(BrandAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.patch("/{asset_id}", response_model=BrandAssetResponse)
async def update_asset(
    asset_id: UUID,
    asset_update: BrandAssetUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(BrandAsset).where(BrandAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    update_data = asset_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset, field, value)

    await db.commit()
    await db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(BrandAsset).where(BrandAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    await db.delete(asset)
    await db.commit()