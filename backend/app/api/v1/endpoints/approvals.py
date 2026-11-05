from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models.brand import Approval, ContentSubmission
from app.schemas.brand import ApprovalCreate, ApprovalResponse

router = APIRouter()


@router.get("", response_model=List[ApprovalResponse])
async def list_approvals(
    skip: int = 0,
    limit: int = 100,
    submission_id: UUID = None,
    approver_id: UUID = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Approval)
    if submission_id:
        query = query.where(Approval.content_submission_id == submission_id)
    if approver_id:
        query = query.where(Approval.approver_id == approver_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    approvals = result.scalars().all()
    return approvals


@router.post("", response_model=ApprovalResponse, status_code=status.HTTP_201_CREATED)
async def create_approval(
    approval_in: ApprovalCreate,
    db: AsyncSession = Depends(get_db),
):
    # Verify submission exists
    result = await db.execute(select(ContentSubmission).where(ContentSubmission.id == approval_in.content_submission_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    approval = Approval(**approval_in.model_dump(), approver_id="00000000-0000-0000-0000-000000000000")  # TODO: Get from auth
    db.add(approval)

    # Update submission status based on approval decision
    if approval_in.decision == "approved":
        submission.status = "approved"
    elif approval_in.decision == "rejected":
        submission.status = "rejected"

    await db.commit()
    await db.refresh(approval)
    return approval


@router.get("/{approval_id}", response_model=ApprovalResponse)
async def get_approval(
    approval_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Approval).where(Approval.id == approval_id))
    approval = result.scalar_one_or_none()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval