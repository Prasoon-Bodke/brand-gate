from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.brand import Review, ContentSubmission
from app.schemas.brand import ReviewCreate, ReviewResponse

router = APIRouter()


@router.get("", response_model=List[ReviewResponse])
async def list_reviews(
    skip: int = 0,
    limit: int = 100,
    submission_id: UUID = None,
    reviewer_id: UUID = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Review)
    if submission_id:
        query = query.where(Review.content_submission_id == submission_id)
    if reviewer_id:
        query = query.where(Review.reviewer_id == reviewer_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    reviews = result.scalars().all()
    return reviews


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_in: ReviewCreate,
    db: AsyncSession = Depends(get_db),
):
    # Verify submission exists
    result = await db.execute(select(ContentSubmission).where(ContentSubmission.id == review_in.content_submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    review = Review(**review_in.model_dump(), reviewer_id="00000000-0000-0000-0000-000000000000")  # TODO: Get from auth
    db.add(review)

    # Update submission status based on review decision
    if review_in.decision == "approve":
        submission.status = "reviewing"
    elif review_in.decision == "request_changes":
        submission.status = "needs_revision"
    elif review_in.decision == "reject":
        submission.status = "rejected"

    await db.commit()
    await db.refresh(review)
    return review


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review