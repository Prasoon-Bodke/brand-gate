import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    Boolean,
    JSON,
    ARRAY,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class UserRole(str, enum.Enum):
    BRAND_ADMIN = "brand_admin"
    CREATOR = "creator"
    REVIEWER = "reviewer"
    APPROVER = "approver"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.CREATOR, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_submissions = relationship("ContentSubmission", back_populates="creator")
    reviews = relationship("Review", back_populates="reviewer")
    approvals = relationship("Approval", back_populates="approver")


class BrandGuideline(Base):
    __tablename__ = "brand_guidelines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # tone, terminology, visual, accessibility, etc.
    rule_text = Column(Text, nullable=False)
    rule_type = Column(String(50), nullable=False)  # deterministic, llm_based, hybrid
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    findings = relationship("Finding", back_populates="guideline")


class ApprovedFact(Base):
    __tablename__ = "approved_facts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fact_text = Column(Text, nullable=False)
    fact_type = Column(String(50), nullable=False)  # claim, statistic, product_info, company_info
    source_url = Column(String(500), nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    embedding = Column(JSON, nullable=True)  # For vector search
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    findings = relationship("Finding", back_populates="approved_fact")


class BrandAsset(Base):
    __tablename__ = "brand_assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    asset_type = Column(String(50), nullable=False)  # logo, color_palette, font, icon, template
    file_path = Column(String(500), nullable=False)
    file_hash = Column(String(64), nullable=False)  # SHA-256
    metadata = Column(JSON, nullable=True)  # Color values, font details, dimensions, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContentSubmission(Base):
    __tablename__ = "content_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content_type = Column(String(50), nullable=False)  # text, image, document, mixed
    original_content = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_hash = Column(String(64), nullable=True)
    metadata = Column(JSON, nullable=True)
    status = Column(String(20), default="pending")  # pending, reviewing, approved, rejected, needs_revision
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="content_submissions")
    findings = relationship("Finding", back_populates="content_submission")
    reviews = relationship("Review", back_populates="content_submission")
    approvals = relationship("Approval", back_populates="content_submission")
    versions = relationship("ContentVersion", back_populates="content_submission")


class ContentVersion(Base):
    __tablename__ = "content_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_submission_id = Column(UUID(as_uuid=True), ForeignKey("content_submissions.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    changes_summary = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    content_submission = relationship("ContentSubmission", back_populates="versions")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_submission_id = Column(UUID(as_uuid=True), ForeignKey("content_submissions.id"), nullable=False)
    guideline_id = Column(UUID(as_uuid=True), ForeignKey("brand_guidelines.id"), nullable=True)
    approved_fact_id = Column(UUID(as_uuid=True), ForeignKey("approved_facts.id"), nullable=True)
    tier = Column(Integer, nullable=False)  # 0, 1, 2
    finding_type = Column(String(50), nullable=False)  # violation, inconsistency, suggestion, info
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    evidence = Column(JSON, nullable=True)  # Supporting evidence from AI
    location = Column(JSON, nullable=True)  # Position in content (char offset, page, etc.)
    confidence = Column(JSON, nullable=True)  # Confidence scores
    suggested_correction = Column(Text, nullable=True)
    correction_reasoning = Column(Text, nullable=True)
    status = Column(String(20), default="open")  # open, acknowledged, resolved, dismissed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_submission = relationship("ContentSubmission", back_populates="findings")
    guideline = relationship("BrandGuideline", back_populates="findings")
    approved_fact = relationship("ApprovedFact", back_populates="findings")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_submission_id = Column(UUID(as_uuid=True), ForeignKey("content_submissions.id"), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    decision = Column(String(20), nullable=False)  # approve, request_changes, reject
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_submission = relationship("ContentSubmission", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_submission_id = Column(UUID(as_uuid=True), ForeignKey("content_submissions.id"), nullable=False)
    approver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    decision = Column(String(20), nullable=False)  # approved, rejected
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    content_submission = relationship("ContentSubmission", back_populates="approvals")
    approver = relationship("User", back_populates="approvals")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)