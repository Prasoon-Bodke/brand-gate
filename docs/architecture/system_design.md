# Brand Gate - System Architecture Design

## Overview

Brand Gate is an AI-powered brand governance platform that reviews content against organizational brand guidelines. The system uses a three-tier AI pipeline to detect brand inconsistencies and provide evidence-backed findings with correction suggestions.

## High-Level Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌──────────────────────┐
│   Next.js       │────▶│   FastAPI       │────▶│   Content Processing │
│   Frontend      │     │   Backend       │     │   & Three-Tier AI    │
└─────────────────┘     └─────────────────┘     └──────────────────────┘
                              │                          │
                              ▼                          ▼
                       ┌─────────────────┐     ┌──────────────────────┐
                       │   PostgreSQL    │     │   Evidence-backed    │
                       │   + pgvector    │     │   Findings           │
                       └─────────────────┘     └──────────────────────┘
                                                          │
                                                          ▼
                                               ┌──────────────────────┐
                                               │   Correction &       │
                                               │   Self-Check         │
                                               └──────────────────────┘
                                                          │
                                                          ▼
                                               ┌──────────────────────┐
                                               │   Human Review &     │
                                               │   Approval Workflow  │
                                               └──────────────────────┘
                                                          │
                                                          ▼
                                               ┌──────────────────────┐
                                               │   Governance         │
                                               │   Analytics          │
                                               └──────────────────────┘
```

## Components

### 1. Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context + Server Components
- **API Communication**: Axios with typed API client

**Key Pages**:
- Dashboard - Overview of submissions, reviews, analytics
- Submission Upload - Drag-drop interface for content
- Review Interface - View findings, evidence, suggestions
- Brand Guidelines Management - CRUD for guidelines, facts, assets
- User Management - Role-based access control
- Analytics - Governance metrics and reports

### 2. Backend (FastAPI)
- **Framework**: FastAPI with async/await
- **Language**: Python 3.11+
- **Database ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Authentication**: JWT with bcrypt password hashing
- **Validation**: Pydantic v2

**API Structure**:
```
/api/v1/
├── auth/           # Authentication (register, login, tokens)
├── users/          # User management
├── guidelines/     # Brand guidelines CRUD
├── facts/          # Approved facts ledger
├── assets/         # Brand assets management
├── submissions/    # Content submissions & versions
├── findings/       # AI findings
├── reviews/        # Review workflow
└── approvals/      # Approval workflow
```

### 3. Database (PostgreSQL + pgvector)
- **Primary DB**: PostgreSQL 15+
- **Vector Search**: pgvector extension for semantic search
- **Full-text Search**: pg_trgm for fuzzy matching
- **Connection Pooling**: PgBouncer (production)

**Key Tables**:
- `users` - User accounts with roles
- `brand_guidelines` - Deterministic and LLM-based rules
- `approved_facts` - Verified claims with embeddings
- `brand_assets` - Logos, colors, fonts, templates
- `content_submissions` - Submitted content for review
- `content_versions` - Version history
- `findings` - AI-detected issues
- `reviews` - Human reviews
- `approvals` - Final approvals
- `audit_logs` - Comprehensive audit trail

### 4. AI Pipeline (Three-Tier)

#### Tier 0: Deterministic Rules
- **Technology**: Custom rule engine, regex, PaddleOCR, Docling
- **Checks**: Banned terms, claim words, readability, colors, fonts, accessibility
- **Characteristics**: Fast, 100% reproducible, no hallucination

#### Tier 1: Jev Decision Model
- **Technology**: Jev by TypeSafe AI
- **Checks**: Brand tone analysis, contextual rule evaluation, structured classification
- **Characteristics**: Confidence-based decisions, explainable

#### Tier 2: Open-weight LLMs
- **Technology**: LiteLLM + Ollama (Qwen 2.5 7B, Llama 3.2 3B)
- **Checks**: Explain findings, generate minimal corrections, preserve meaning, recheck corrections
- **Characteristics**: Generative, requires self-check, local inference for privacy

## Data Flow

### Content Submission Flow
1. User uploads content via frontend
2. Backend creates `ContentSubmission` record
3. Content Processing Service extracts text/images
4. Three-tier AI pipeline runs sequentially:
   - Tier 0: Fast deterministic checks
   - Tier 1: Jev decision model
   - Tier 2: LLM explanation and correction
5. Findings stored with evidence and confidence scores
6. Submission status updated to "reviewing"
7. Reviewers notified

### Review Flow
1. Reviewer views submission with findings
2. Reviewer can: acknowledge, dismiss, or request changes
3. Review decision recorded
4. If "request_changes": Creator notified, new version created
4. If "approve": Moves to approval stage

### Approval Flow
1. Approver reviews submission and all findings/reviews
2. Approver decides: approved or rejected
3. Decision recorded with comments
4. Final status updated
5. Audit log entry created

## Security Considerations

- **Authentication**: JWT tokens with short expiry, refresh token rotation
- **Authorization**: Role-based access control (RBAC)
- **Data Privacy**: Confidential content processed locally via Ollama
- **Audit Trail**: All actions logged with user, timestamp, IP
- **Secrets Management**: Environment variables, never in code
- **CORS**: Configured for frontend domain only
- **Rate Limiting**: API rate limiting per user/IP

## Scalability Considerations

- **Horizontal Scaling**: Stateless FastAPI workers behind load balancer
- **Database**: Read replicas for analytics, connection pooling
- **AI Pipeline**: Async task queue (Celery + Redis) for background processing
- **Caching**: Redis for session, rate limits, frequent queries
- **File Storage**: S3-compatible for assets and uploads
- **Monitoring**: Prometheus + Grafana, structured logging

## Deployment Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CDN       │────▶│   Load      │────▶│   Frontend  │
│   (Vercel)  │     │   Balancer  │     │   (Next.js) │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   API       │
                   │   Gateway   │
                   └─────────────┘
                          │
           ┌──────────────┼──────────────┐
           ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ Backend  │   │ Backend  │   │ Backend  │
    │ Worker 1 │   │ Worker 2 │   │ Worker N │
    └──────────┘   └──────────┘   └──────────┘
           │              │              │
           └──────────────┼──────────────┘
                          ▼
              ┌─────────────────────┐
              │   PostgreSQL +      │
              │   pgvector          │
              │   (Primary + Reads) │
              └─────────────────────┘
                          │
           ┌──────────────┼──────────────┐
           ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Redis   │   │  Ollama  │   │  S3/MinIO│
    │ (Cache,  │   │ (Local   │   │ (Assets, │
    │  Queue)  │   │   LLM)   │   │  Uploads)│
    └──────────┘   └──────────┘   └──────────┘
```

## Technology Stack Summary

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | Next.js | 14.2 |
| Frontend | React | 18.2 |
| Frontend | TypeScript | 5.3 |
| Frontend | Tailwind CSS | 3.4 |
| Backend | FastAPI | 0.109 |
| Backend | Python | 3.11+ |
| Backend | SQLAlchemy | 2.0 |
| Backend | Pydantic | 2.5 |
| Database | PostgreSQL | 15+ |
| Vector Search | pgvector | 0.5+ |
| AI - Tier 1 | Jev | Latest |
| AI - Tier 2 | LiteLLM + Ollama | Latest |
| AI - Models | Qwen 2.5 7B, Llama 3.2 3B | Latest |
| Document Processing | Docling | 1.8 |
| OCR | PaddleOCR | 2.7 |
| Image Matching | SigLIP | Latest |
| Auth | JWT + bcrypt | - |
| Migrations | Alembic | 1.13 |
| Testing | pytest | 7.4 |
| Monitoring | Prometheus + Grafana | - |