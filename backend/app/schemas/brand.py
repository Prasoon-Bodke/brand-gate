from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    BRAND_ADMIN = "brand_admin"
    CREATOR = "creator"
    REVIEWER = "reviewer"
    APPROVER = "approver"


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.CREATOR


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class BrandGuidelineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=100)
    rule_text: str
    rule_type: str = Field(..., pattern="^(deterministic|llm_based|hybrid)$")
    severity: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    is_active: bool = True


class BrandGuidelineCreate(BrandGuidelineBase):
    pass


class BrandGuidelineUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    rule_text: Optional[str] = None
    rule_type: Optional[str] = Field(None, pattern="^(deterministic|llm_based|hybrid)$")
    severity: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    is_active: Optional[bool] = None


class BrandGuidelineResponse(BrandGuidelineBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApprovedFactBase(BaseModel):
    fact_text: str
    fact_type: str = Field(..., pattern="^(claim|statistic|product_info|company_info)$")
    source_url: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    is_active: bool = True


class ApprovedFactCreate(ApprovedFactBase):
    pass


class ApprovedFactUpdate(BaseModel):
    fact_text: Optional[str] = None
    fact_type: Optional[str] = Field(None, pattern="^(claim|statistic|product_info|company_info)$")
    source_url: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ApprovedFactResponse(ApprovedFactBase):
    id: UUID
    embedding: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BrandAssetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    asset_type: str = Field(..., pattern="^(logo|color_palette|font|icon|template)$")
    file_path: str
    file_hash: str = Field(..., min_length=64, max_length=64)
    metadata: Optional[Dict[str, Any]] = None
    is_active: bool = True


class BrandAssetCreate(BrandAssetBase):
    pass


class BrandAssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    asset_type: Optional[str] = Field(None, pattern="^(logo|color_palette|font|icon|template)$")
    metadata: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class BrandAssetResponse(BrandAssetBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentSubmissionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., pattern="^(text|image|document|mixed)$")
    original_content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ContentSubmissionCreate(ContentSubmissionBase):
    pass


class ContentSubmissionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    original_content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, pattern="^(pending|reviewing|approved|rejected|needs_revision)$")


class ContentSubmissionResponse(ContentSubmissionBase):
    id: UUID
    file_path: Optional[str] = None
    file_hash: Optional[str] = None
    status: str
    creator_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentVersionBase(BaseModel):
    version_number: int
    content: str
    changes_summary: Optional[str] = None


class ContentVersionCreate(ContentVersionBase):
    pass


class ContentVersionResponse(ContentVersionBase):
    id: UUID
    content_submission_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class FindingBase(BaseModel):
    tier: int = Field(..., ge=0, le=2)
    finding_type: str = Field(..., pattern="^(violation|inconsistency|suggestion|info)$")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    evidence: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None
    confidence: Optional[Dict[str, Any]] = None
    suggested_correction: Optional[str] = None
    correction_reasoning: Optional[str] = None


class FindingCreate(FindingBase):
    content_submission_id: UUID
    guideline_id: Optional[UUID] = None
    approved_fact_id: Optional[UUID] = None


class FindingUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(open|acknowledged|resolved|dismissed)$")
    suggested_correction: Optional[str] = None
    correction_reasoning: Optional[str] = None


class FindingResponse(FindingBase):
    id: UUID
    content_submission_id: UUID
    guideline_id: Optional[UUID] = None
    approved_fact_id: Optional[UUID] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    decision: str = Field(..., pattern="^(approve|request_changes|reject)$")
    comments: Optional[str] = None


class ReviewCreate(ReviewBase):
    content_submission_id: UUID


class ReviewResponse(ReviewBase):
    id: UUID
    content_submission_id: UUID
    reviewer_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApprovalBase(BaseModel):
    decision: str = Field(..., pattern="^(approved|rejected)$")
    comments: Optional[str] = None


class ApprovalCreate(ApprovalBase):
    content_submission_id: UUID


class ApprovalResponse(ApprovalBase):
    id: UUID
    content_submission_id: UUID
    approver_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    action: str
    resource_type: str
    resource_id: Optional[UUID] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True