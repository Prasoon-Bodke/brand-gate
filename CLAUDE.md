# Brand Gate - CLAUDE.md

This document serves as the primary instruction manual for Claude Code when working on the Brand Gate repository.

---

## 1. Project Overview

**Brand Gate** is an AI-powered brand governance platform that reviews posts, advertisements, images, and documents against an organization's approved brand guidelines, facts, and visual assets. It detects brand inconsistencies, explains each issue with supporting evidence, and suggests corrections while keeping humans in control of final approval.

---

## 2. Project Objectives

- Prevent unsupported promotional claims in published content
- Maintain consistent brand identity across all content sources
- Detect outdated company information and incorrect logo/colour usage
- Ensure accessibility compliance (WCAG AA/AAA)
- Provide evidence-backed AI findings with human oversight

---

## 3. Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **Frontend** | Next.js | 14.2 |
| **Frontend** | React | 18.2 |
| **Frontend** | TypeScript | 5.3 |
| **Frontend** | Tailwind CSS | 3.4 |
| **Backend** | FastAPI | 0.109 |
| **Backend** | Python | 3.11+ |
| **Backend** | SQLAlchemy | 2.0 |
| **Database** | PostgreSQL | 15+ |
| **Vector Search** | pgvector | 0.5+ |
| **AI - Tier 1** | Jev | Latest |
| **AI - Tier 2** | LiteLLM + Ollama | Latest |
| **Model** | Qwen 2.5 7B / Llama 3.2 3B | Latest |
| **Document Processing** | Docling | 1.8 |
| **OCR** | PaddleOCR | 2.7 |
| **Image Matching** | SigLIP | Latest |
| **Migrations** | Alembic | 1.13 |
| **Testing** | pytest | 7.4 |

---

## 4. System Architecture

### Four-Layer Architecture

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
```

### Three-Tier AI Pipeline

**Tier 0 — Deterministic Rules**
- Banned and outdated terminology
- Claim-word detection
- Readability checks
- Brand colour and font checks
- Accessibility and contrast checks

**Tier 1 — Jev Decision Model**
- Brand tone analysis
- Contextual rule evaluation
- Structured classification
- Confidence-based decisions

**Tier 2 — Open-weight LLM**
- Explain detected issues
- Generate minimal corrections
- Preserve original meaning
- Recheck suggested corrections

---

## 5. Repository Structure

```
brand-gate/
├── frontend/                      # Next.js frontend
│   ├── src/
│   │   ├── app/                   # App Router pages
│   │   ├── components/            # Reusable UI components
│   │   ├── lib/                   # Utilities, API client
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── types/                 # TypeScript type definitions
│   │   ├── styles/                # Global styles
│   │   └── store/                 # Zustand state (if needed)
│   ├── public/                    # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── tailwind.config.js
│
├── backend/                       # FastAPI backend
│   ├── app/
│   │   ├── api/                   # API routes (v1)
│   │   ├── core/                  # Config, security, database
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── services/              # Business logic services
│   │   ├── db/                    # Database utilities
│   │   ├── utils/                 # Helpers and utilities
│   │   └── workers/               # Background task workers
│   ├── migrations/                # Alembic migrations
│   ├── tests/                     # Test suite
│   ├── requirements.txt
│   └── main.py
│
├── database/                      # Database schemas & sample data
│   ├── schema.sql                 # PostgreSQL schema with constraints
│   └── sample_data.sql            # Development/test data
│
├── datasets/                      # Training and test data
│   ├── brand_guidelines/          # Rule definitions (JSON)
│   ├── approved_facts/              # Verified claims ledger
│   ├── brand_assets/              # Logos, colors, fonts
│   └── test_content/              # Test submissions
│
├── docs/                          # Documentation
│   ├── architecture/              # System design docs
│   ├── api/                       # API reference
│   ├── development/               # Developer guides
│   └── deployment/                # Deployment instructions
│
├── scripts/                       # Utility scripts
│   ├── verify_environment.py      # Environment check script
│   └── seed_database.py           # Database seeding
│
├── tests/                         # End-to-end tests
│   └── unit/                      # E2E test cases
│
├── .env.example                   # Environment template
├── .gitignore
├── CLAUDE.md                      # This file
└── README.md                      # Project overview
```

---

## 6. Frontend Development Guidelines

### Component Structure
```typescript
interface ComponentProps {
  // Use TypeScript interfaces, not types for props
}

export const ComponentName: React.FC<ComponentProps> = ({ ... }) => {
  // Always use proper typing
  const [state, setState] = useState<null | string>(null);
  
  return (
    <div className="...">
      {/* Use Tailwind CSS */}
    </div>
  );
};
```

### API Client
- Use Axios or native fetch for API calls
- Create typed API client in `src/lib/api.ts`
- Always handle errors appropriately
- Use abort signals for cancellable requests

### State Management
- Prefer React Server Components for server data
- Use client components for interactive features
- Local state: React useState/useReducer
- Global state: Zustand or React Context

### Styling
- Tailwind CSS for styling
- Mobile-first responsive design
- Dark mode support (system preference)
- Consistent spacing: 4px scale (gap-1, gap-2, etc.)

### File Naming
- Components: PascalCase: `Button.tsx`, `UserCard.tsx`
- Hooks: usePrefix: `useApi.ts`, `useAuth.ts`
- Types: PascalCase: `User.ts`, `Submission.ts`
- Utils: camelCase: `api.ts`, `validation.ts`

---

## 7. Backend Development Guidelines

### Project Structure
```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/    # Route handlers
│   │   └── api.py        # Router aggregation
├── core/
│   ├── config.py         # Settings management
│   ├── security.py       # Auth utilities
│   └── database.py       # DB connection
├── models/               # SQLAlchemy models
├── schemas/              # Pydantic schemas
├── services/             # Business logic
└── utils/                # Helpers
```

### API Design
- Use FastAPI path operations as "services"
- Separate routes (endpoints) from business logic (services)
- Use dependency injection for database sessions
- Apply proper error handling with HTTPException

### Database Models
- Use SQLAlchemy 2.0 style with `mapped_column`
- Inherit from `Base` declarative base
- Define indexes in `__table_args__`
- Use UUIDs for primary keys

### Request/Response Schemas
- All inputs: Pydantic models (validates + coerces)
- All outputs: Pydantic response models
- Use `model_dump(exclude={"field"})` to hide sensitive data
- Enable `from_attributes = True` for ORM compatibility

---

## 8. Database Design and Guidelines

### Database Schema

The database uses PostgreSQL with pgvector for semantic search.

**Core Tables:**

| Table | Description | Key Fields |
|-------|-------------|------------|
| `users` | User accounts | email, hashed_password, role |
| `brand_guidelines` | Brand rules | name, category, rule_text, severity |
| `approved_facts` | Verified claims | fact_text, fact_type, embedding |
| `brand_assets` | Visual assets | name, asset_type, file_hash |
| `content_submissions` | Submitted content | title, content_type, status |
| `content_versions` | Content history | version_number, content |
| `findings` | AI detections | tier, severity, title, evidence |
| `reviews` | Human reviews | decision, comments |
| `approvals` | Final approvals | decision, comments |
| `audit_logs` | Audit trail | action, resource_type, details |

### Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add new feature"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Show history
alembic history
```

**Migration Best Practices:**
- Always use `--autogenerate` for schema changes
- Write migration comments in imperative mood
- Include data migrations in separate scripts
- Test migrations on fresh database

---

## 9. API Development Standards

### RESTful Conventions

| Method | Purpose | Example |
|--------|---------|---------|
| GET | Retrieve | `GET /submissions/{id}` |
| POST | Create | `POST /submissions` |
| PATCH | Partial update | `PATCH /submissions/1` |
| PUT | Full replace | `PUT /submissions/1` |
| DELETE | Remove | `DELETE /submissions/1` |

### Error Response Format

```json
{
  "detail": "Human-readable error message"
}
```

For validation errors:

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

### Pagination

```
GET /items?skip=0&limit=100
```

Default: `skip=0, limit=100` (max: 1000)

### Filtering

Common query parameters:
- `is_active` (boolean)
- `status` (string)
- `category` (string)
- `created_after` (ISO datetime)

### Rate Limiting

- Default: 100 requests/minute per user
- Returns 429 when exceeded
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

---

## 10. Coding Conventions

### Backend (Python)

```python
# Formatting
- Black for code formatting
- Ruff for linting and isort
- Type hints on all function parameters

# Imports
from app.core.config import settings  # Project imports first
from fastapi import APIRouter, Depends  # External imports second
from typing import Optional  # Standard library third

# Function signatures
def process_content(
    content: str,
    options: ProcessOptions = ProcessOptions(),
) -> ProcessingResult:
    """
    Brief one-line summary.
    
    Longer description if needed.
    
    Args:
        content: The content to process
        options: Processing configuration
    
    Returns:
        ProcessingResult with findings
    
    Raises:
        ValueError: If content is empty
    """
    ...

# Database queries (async)
result = await session.execute(
    select(BrandGuideline)
    .where(BrandGuideline.category == category)
    .order_by(BrandGuideline.created_at.desc())
)
guidelines = result.scalars().all()
```

### Frontend (TypeScript)

```typescript
// File: src/components/Button.tsx
import * as React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  onClick: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
}) => {
  return (
    <button
      className={cn(
        'rounded-md font-medium transition-colors',
        variant === 'primary' && 'bg-blue-500 text-white',
        variant === 'secondary' && 'bg-gray-200 text-gray-800',
        size === 'sm' && 'px-2 py-1 text-sm',
        size === 'md' && 'px-4 py-2 text-base',
        size === 'lg' && 'px-6 py-3 text-lg'
      )}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

---

## 11. Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | snake_case | `user_service.py`, `content_parser.py` |
| Classes | PascalCase | `UserService`, `ContentSubmission` |
| Functions | snake_case | `process_content()`, `get_user_by_id()` |
| Constants | UPPER_SNAKE_CASE | `MAX_CONTENT_LENGTH`, `DEFAULT_PAGE_SIZE` |
| Variables | snake_case | `user_id`, `content_text` |
| Environment vars | UPPER_SNAKE_CASE | `DATABASE_URL`, `API_KEY` |

---

## 12. Error Handling

### Backend

```python
from fastapi import HTTPException, status

# Validate input
if not title:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Title is required"
    )

# Handle not found
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

# Handle conflicts
if existing_email:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Email already registered"
    )
```

### Frontend

```typescript
// API client with error handling
try {
  const response = await api.get<Submission>('/submissions/1');
  return response.data;
} catch (error) {
  if (error.response?.status === 404) {
    // Handle not found
    toast.error('Submission not found');
  } else if (error.response?.status === 401) {
    // Handle unauthorized - redirect to login
    router.push('/login');
  } else {
    // Handle other errors
    toast.error(error.response?.data.detail || 'Something went wrong');
  }
  throw error;
}
```

---

## 13. Security Guidelines

### Authentication & Authorization
- Always use JWT tokens for authentication
- Validate tokens on every protected endpoint
- Use role-based access control (RBAC)
- Never trust client-side role checks

### Secrets Management
- **NEVER** hardcode API keys, passwords, or secrets in code
- Use `.env` files (git-ignored) for local development
- Use environment variables in production (Kubernetes secrets, AWS SSM, etc.)
- Validate required env vars at startup

### Data Security
- Hash passwords with bcrypt (12 rounds minimum)
- Encrypt sensitive data at rest
- Use HTTPS in production
- Implement proper CORS policies
- Rate limit API endpoints

### Audit Logging
- Log all user actions with user ID, timestamp, IP
- Log data access and modifications
- Store logs securely for compliance

### Responsible AI
- AI suggestions are never applied automatically
- Humans retain final approval authority
- Uncertain findings escalated for human review
- Confidential content processed locally via Ollama

---

## 14. Environment Variables

### Required Variables

```env
# General
NODE_ENV=development
ENVIRONMENT=development
LOG_LEVEL=info

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=

# Backend
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/brand_gate

# AI Pipeline
JEV_MODEL_ENDPOINT=http://localhost:8001/jev
LITELLM_MASTER_KEY=
OLLAMA_BASE_URL=http://localhost:11434
QWEN_LLM_MODEL=qwen2.5:7b
LLAMA_LLM_MODEL=llama3.2:3b

# Security
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Configuration Loading

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://..."
    SECRET_KEY: str = "change-me"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## 15. Git and Branching Strategy

### Branching Model

```
main (production) ←─── release/v1.0.0
     ↑
develop ←─── feature/new-feature
     ↑
     └── feature/another-feature
```

### Branch Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Feature | `feature/short-description` | `feature/add-user-auth` |
| Bug Fix | `fix/short-description` | `fix/login-error` |
| Hotfix | `hotfix/short-description` | `hotfix/critical-bug` |
| Release | `release/vX.Y.Z` | `release/v1.0.0` |

### Commit Message Format (Conventional Commits)

```
type(scope): short description

longer description if needed

Co-Authored-By: Claude Code <noreply@anthropic.com>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(auth): add JWT authentication`
- `fix(api): handle not found errors properly`
- `docs(readme): update installation instructions`

### Pull Request Guidelines

1. Create PR from feature branch to `main`
2. Fill out PR description with:
   - Summary of changes
   - Why changes were needed
   - Screenshots for UI changes
3. Self-review code before submitting
4. Request review from team members
5. Resolve all comments before merging
6. Squash commits before merge

---

## 16. Testing Guidelines

### Test Structure

```
backend/tests/
├── unit/          # Unit tests
│   └── test_models.py
├── integration/   # Integration tests
└── conftest.py    # Pytest configuration

frontend/
├── __tests__/     # Jest tests
│   ├── components/
│   ├── hooks/
│   └── pages/
└── jest.config.js
```

### Backend Tests (pytest)

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_read_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Item 1"}
```

### Frontend Tests (Jest + React Testing Library)

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../components/Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button onClick={() => {}}>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByText('Click'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});
```

### Running Tests

```bash
# Backend
cd backend
pytest                    # All tests
pytest -v                 # Verbose
pytest --cov=app          # With coverage

# Frontend
cd frontend
npm test                  # Interactive mode
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report
```

---

## 17. Development Workflow

### Daily Workflow

1. Pull latest changes
   ```bash
   git pull origin main
   ```

2. Create feature branch
   ```bash
   git checkout -b feature/your-feature-name
   git push -u origin feature/your-feature-name
   ```

3. Implement changes with tests
4. Commit with conventional messages
5. Push changes
6. Create Pull Request
7. Address review comments
8. Merge when approved

### Starting Development

```bash
# 1. Verify environment
python scripts/verify_environment.py

# 2. Start services
docker-compose up -d postgres
ollama serve
uvicorn app.main:app --reload &

# 3. Run migrations
cd backend && alembic upgrade head

# 4. Start dev servers
# Frontend: cd frontend && npm run dev
# Backend: cd backend && uvicorn app.main:app --reload

# 5. Verify
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 18. Docker Instructions

### Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up --build
```

### Production

```dockerfile
# Dockerfile (backend)
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile (frontend)
FROM node:20-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package*.json ./
RUN npm ci --omit=dev
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 19. Documentation Guidelines

### Code Documentation

```python
def analyze_brand_tone(content: str) -> ToneAnalysis:
    """
    Analyze content for brand tone alignment.
    
    Uses Jev decision model to classify tone and identify deviations
    from brand personality guidelines.
    
    Args:
        content: Text content to analyze
        
    Returns:
        ToneAnalysis with tone classification and confidence scores
        
    Example:
        >>> result = analyze_brand_tone("We are the best!")
        >>> print(result.tone_score)
        0.75
    """
    ...
```

### API Documentation

Use docstrings for FastAPI to auto-generate OpenAPI spec:

```python
@app.post("/content", response_model=FindingResponse)
async def create_finding(
    finding_in: FindingCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new finding from AI analysis.
    
    A finding represents an issue detected in content submission,
    such as a brand guideline violation or inconsistency.
    
    Args:
        finding_in: Finding creation data
        db: Database session
        
    Returns:
        The created FindingRecord
    """
    ...
```

### Documentation Files

- `README.md` - Project overview, quick start
- `docs/architecture/` - System design, data flow
- `docs/api/` - API reference (auto-generated from OpenAPI)
- `docs/development/` - Developer guides, setup
- `CLAUDE.md` - This file (AI development guide)

---

## 20. Important Rules for Claude Code

### Understanding Before Modifying

1. **ALWAYS** read existing code before making changes
2. **SEARCH** for existing implementations across the codebase
3. **ASK** if requirements are unclear
4. **EXPLAIN** significant architectural decisions in PRs

### Development Principles

1. **Write modular, reusable code**
   - Extract common patterns into utilities
   - Use composition over inheritance
   - Keep functions focused on single responsibility

2. **Avoid unnecessary dependencies**
   - Justify each new dependency
   - Prefer built-in libraries when possible
   - Audit dependencies for security

3. **Never hardcode secrets**
   - Use environment variables
   - Validate required vars at startup
   - Mask secrets in logs

4. **Maintain consistent naming**
   - Follow established conventions
   - Be descriptive, not ambiguous
   - Use domain terminology

5. **Proper error handling**
   - Validate all inputs
   - Use appropriate HTTP status codes
   - Provide actionable error messages

6. **Write tests for new functionality**
   - Unit tests for business logic
   - Integration tests for API endpoints
   - Test edge cases and error paths

7. **Update documentation**
   - Update API docs for changes
   - Add code comments for complex logic
   - Update README if needed

8. **Avoid duplicating existing functionality**
   - Search before implementing
   - Refactor to reduce duplication
   - Share common code

9. **Never modify unrelated files**
   - Focus on the task at hand
   - Make atomic commits
   - Request review for complex changes

10. **Never delete existing functionality without permission**
    - Get explicit approval first
    - Document why removal is needed
    - Consider deprecation period

---

## Quick Reference

### Common Commands

```bash
# Backend
cd backend && uvicorn app.main:app --reload
alembic revision --autogenerate -m "message"
alembic upgrade head
pytest

# Frontend
cd frontend && npm run dev
npm run lint
npm run type-check
npm test

# Database
psql -h localhost -U postgres -d brand_gate
alembic upgrade head
docker-compose up postgres

# Testing
python scripts/verify_environment.py
pytest --cov=app
```

### File Locations

- **Backend Entry**: `backend/app/main.py`
- **Frontend Entry**: `frontend/src/app/page.tsx`
- **Models**: `backend/app/models/brand.py`
- **Schemas**: `backend/app/schemas/brand.py`
- **API Routes**: `backend/app/api/v1/endpoints/`
- **Tests**: `backend/tests/`

---

*Document version: 1.0.0*
*Last updated: 2026-11-05*