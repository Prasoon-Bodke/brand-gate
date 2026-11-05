# Brand Gate - API Reference

## Base URL
- Development: `http://localhost:8000/api/v1`
- Production: `https://api.brandgate.com/api/v1`

## Authentication

All API endpoints (except auth) require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Get Access Token
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secret
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "role": "creator"
}
```

---

## Users

### List Users
```http
GET /users?skip=0&limit=100
```

### Get User
```http
GET /users/{user_id}
```

### Update User
```http
PATCH /users/{user_id}
Content-Type: application/json

{
  "full_name": "Jane Doe",
  "role": "reviewer"
}
```

### Delete User
```http
DELETE /users/{user_id}
```

---

## Brand Guidelines

### List Guidelines
```http
GET /guidelines?skip=0&limit=100&category=terminology&is_active=true
```

### Create Guideline
```http
POST /guidelines
Content-Type: application/json

{
  "name": "No Superlatives",
  "description": "Avoid using superlative claims without evidence",
  "category": "terminology",
  "rule_text": "Do not use words like best, greatest, ultimate without supporting data",
  "rule_type": "deterministic",
  "severity": "high",
  "is_active": true
}
```

### Get Guideline
```http
GET /guidelines/{guideline_id}
```

### Update Guideline
```http
PATCH /guidelines/{guideline_id}
Content-Type: application/json

{
  "severity": "critical",
  "is_active": true
}
```

### Delete Guideline
```http
DELETE /guidelines/{guideline_id}
```

---

## Approved Facts

### List Facts
```http
GET /facts?skip=0&limit=100&fact_type=claim&is_active=true
```

### Create Fact
```http
POST /facts
Content-Type: application/json

{
  "fact_text": "BrandGate Pro processes up to 10,000 content items per hour",
  "fact_type": "claim",
  "source_url": "https://docs.brandgate.com/performance",
  "tags": ["performance", "pro"],
  "is_active": true
}
```

### Get Fact
```http
GET /facts/{fact_id}
```

### Update Fact
```http
PATCH /facts/{fact_id}
Content-Type: application/json

{
  "tags": ["performance", "pro", "throughput"]
}
```

### Delete Fact
```http
DELETE /facts/{fact_id}
```

---

## Brand Assets

### List Assets
```http
GET /assets?skip=0&limit=100&asset_type=logo&is_active=true
```

### Create Asset
```http
POST /assets
Content-Type: application/json

{
  "name": "Primary Logo",
  "asset_type": "logo",
  "file_path": "/assets/logos/primary.svg",
  "file_hash": "a1b2c3d4e5f6...",
  "metadata": {"colors": ["#1E3A8A", "#3B82F6"]},
  "is_active": true
}
```

### Get Asset
```http
GET /assets/{asset_id}
```

### Update Asset
```http
PATCH /assets/{asset_id}
Content-Type: application/json

{
  "metadata": {"colors": ["#1E3A8A", "#3B82F6"], "updated": true}
}
```

### Delete Asset
```http
DELETE /assets/{asset_id}
```

---

## Content Submissions

### List Submissions
```http
GET /submissions?skip=0&limit=100&status=pending&creator_id=uuid
```

### Create Submission
```http
POST /submissions
Content-Type: application/json

{
  "title": "Q4 Marketing Campaign",
  "content_type": "mixed",
  "original_content": "Campaign content here...",
  "metadata": {"campaign": "Q4-2024", "channel": "social"}
}
```

### Get Submission
```http
GET /submissions/{submission_id}
```

### Update Submission
```http
PATCH /submissions/{submission_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "status": "needs_revision"
}
```

### Delete Submission
```http
DELETE /submissions/{submission_id}
```

### List Versions
```http
GET /submissions/{submission_id}/versions
```

### Create Version
```http
POST /submissions/{submission_id}/versions
Content-Type: application/json

{
  "version_number": 2,
  "content": "Updated content...",
  "changes_summary": "Fixed superlative violations"
}
```

---

## Findings

### List Findings
```http
GET /findings?skip=0&limit=100&submission_id=uuid&tier=0&status=open
```

### Create Finding
```http
POST /findings
Content-Type: application/json

{
  "content_submission_id": "uuid",
  "guideline_id": "uuid",
  "tier": 0,
  "finding_type": "violation",
  "severity": "high",
  "title": "Unsubstantiated Superlative",
  "description": "The word 'ultimate' is used without supporting evidence",
  "evidence": {"matched_word": "ultimate"},
  "location": {"start_offset": 85, "end_offset": 93},
  "confidence": {"score": 1.0},
  "suggested_correction": "Remove 'ultimate' or add supporting data",
  "correction_reasoning": "Superlative claims require evidence per brand guidelines"
}
```

### Get Finding
```http
GET /findings/{finding_id}
```

### Update Finding
```http
PATCH /findings/{finding_id}
Content-Type: application/json

{
  "status": "acknowledged",
  "suggested_correction": "Use 'leading' instead"
}
```

### Delete Finding
```http
DELETE /findings/{finding_id}
```

---

## Reviews

### List Reviews
```http
GET /reviews?skip=0&limit=100&submission_id=uuid&reviewer_id=uuid
```

### Create Review
```http
POST /reviews
Content-Type: application/json

{
  "content_submission_id": "uuid",
  "decision": "request_changes",
  "comments": "Please address the superlative violations before proceeding."
}
```

### Get Review
```http
GET /reviews/{review_id}
```

---

## Approvals

### List Approvals
```http
GET /approvals?skip=0&limit=100&submission_id=uuid&approver_id=uuid
```

### Create Approval
```http
POST /approvals
Content-Type: application/json

{
  "content_submission_id": "uuid",
  "decision": "approved",
  "comments": "Content meets all brand guidelines."
}
```

### Get Approval
```http
GET /approvals/{approval_id}
```

---

## Error Responses

All endpoints may return these error formats:

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- Default: 100 requests/minute per user
- Exceeding limit returns 429 Too Many Requests
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Pagination

List endpoints support:
- `skip` (default: 0)
- `limit` (default: 100, max: 1000)

Response includes:
```json
{
  "items": [...],
  "total": 250,
  "skip": 0,
  "limit": 100
}
```

---

## Filtering

Common filter parameters:
- `is_active` (boolean)
- `category` (string)
- `status` (string)
- `tier` (integer 0-2)
- `created_after` (ISO datetime)
- `created_before` (ISO datetime)

---

## Webhooks (Future)

Planned webhook events:
- `submission.created`
- `submission.findings_completed`
- `review.created`
- `approval.created`
- `content.approved`
- `content.rejected`