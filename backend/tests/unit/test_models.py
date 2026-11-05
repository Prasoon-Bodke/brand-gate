"""Unit tests for SQLAlchemy models."""
import pytest
from uuid import uuid4
from app.models.brand import User, BrandGuideline, ContentSubmission, UserRole


def test_user_role_enum():
    """Test UserRole enum values."""
    assert UserRole.BRAND_ADMIN.value == "brand_admin"
    assert UserRole.CREATOR.value == "creator"
    assert UserRole.REVIEWER.value == "reviewer"
    assert UserRole.APPROVER.value == "approver"


def test_user_model_defaults():
    """Test User model default values."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
    )
    assert user.role == UserRole.CREATOR
    assert user.is_active is True


def test_guideline_severity_validation():
    """Test BrandGuideline severity field."""
    from app.models.brand import BrandGuideline

    guideline = BrandGuideline(
        name="Test Guideline",
        category="terminology",
        rule_text="Test rule",
        rule_type="deterministic",
        severity="high",
    )
    assert guideline.severity == "high"


def test_content_type_validation():
    """Test ContentSubmission content_type field."""
    submission = ContentSubmission(
        title="Test",
        content_type="text",
        creator_id=uuid4(),
    )
    assert submission.content_type == "text"
    assert submission.status == "pending"