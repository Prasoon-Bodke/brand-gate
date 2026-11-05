from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.brand import ContentSubmission, ContentVersion
from app.schemas.brand import ContentSubmissionCreate, ContentSubmissionUpdate, ContentSubmissionResponse, ContentVersionCreate, ContentVersionResponse

router = APIRouter()


@router.get("", response_model=List[ContentSubmissionResponse])
async def list_submissions(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    creator_id: UUID = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(ContentSubmission)
    if status_filter:
        query = query.where(ContentSubmission.status == status_filter)
    if creator_id:
        query = query.where(ContentSubmission.creator_id == creator_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    submissions = result.scalars().all()
    return submissions


@router.post("", response_model=ContentSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(
    submission_in: ContentSubmissionCreate,
    db: AsyncSession = Depends(get_db),
):
    # TODO: Get creator_id from authenticated user
    submission = ContentSubmission(**submission_in.model_dump(), creator_id="00000000-0000-0000-0000-000000000000")
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return submission


@router.get("/{submission_id}", response_model=ContentSubmissionResponse)
async def get_submission(
    submission_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ContentSubmission).where(ContentSubmission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


@router.patch("/{submission_id}", response_model=ContentSubmissionResponse)
async def update_submission(
    submission_id: UUID,
    submission_update: ContentSubmissionUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ContentSubmission).where(ContentSubmission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    update_data = submission_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(submission, field, value)

    await db.commit()
    await db.refresh(submission)
    return submission


@router.delete("/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_submission(
    submission_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ContentSubmission).where(ContentSubmission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    await db.delete(submission)
    await db.commit()


# Content Versions
@router.get("/{submission_id}/versions", response_model=List[ContentVersionResponse])
async def list_versions(
    submission_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ContentVersion).where(ContentVersion.content_submission_id == submission_id)
        .order_by(ContentVersion.version_number)
    )
    versions = result.scalars().all()
    return versions


@router.post("/{submission_id}/versions", response_model=ContentVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_version(
    submission_id: UUID,
    version_in: ContentVersionCreate,
    db: AsyncSession = Depends(get_db),
):
    # Verify submission exists
    result = await db.execute(select(ContentSubmission).where(ContentSubmission.id == submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    version = ContentVersion(
        **version_in.model_dump(),
        content_submission_id=submission_id,
        created_by="00000000-0000-0000-0000-000000000000"  # TODO: Get from auth
    )
    db.add(version)
    await db.commit()
    await db.refresh(version)
    return version