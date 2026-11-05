# Brand Gate - Development Setup

## Prerequisites

- **Node.js**: 20.x LTS
- **Python**: 3.11+
- **PostgreSQL**: 15+ with pgvector extension
- **Docker**: 24+ (for containerized services)
- **Ollama**: For local LLM inference
- **Git**: 2.40+

## Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd brand-gate
```

### 2. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit with your configuration
vim .env
```

Required environment variables:
```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/brand_gate

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# AI Services
OLLAMA_BASE_URL=http://localhost:11434
LITELLM_MASTER_KEY=your-key
```

### 3. Database Setup

#### Option A: Docker (Recommended)
```bash
# Start PostgreSQL with pgvector
docker run -d \
  --name brand-gate-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=brand_gate \
  -p 5432:5432 \
  pgvector/pgvector:pg15

# Run migrations
cd backend
alembic upgrade head

# Load sample data
psql -h localhost -U postgres -d brand_gate -f ../database/sample_data.sql
```

#### Option B: Local PostgreSQL
```bash
# Install pgvector extension
# CREATE EXTENSION vector;

# Run migrations
cd backend
alembic upgrade head
```

### 4. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 6. AI Services Setup

#### Ollama (Local LLM)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
ollama serve

# Pull required models
ollama pull qwen2.5:7b
ollama pull llama3.2:3b
```

#### LiteLLM (Optional - for model routing)
```bash
# Using Docker
docker run -d \
  -p 4000:4000 \
  -e LITELLM_MASTER_KEY=your-key \
  ghcr.io/berriai/litellm:main-latest
```

## Development Workflow

### Running Tests

#### Backend Tests
```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose
pytest --cov=app          # With coverage
pytest tests/unit         # Unit tests only
pytest tests/integration  # Integration tests only
```

#### Frontend Tests
```bash
cd frontend
npm test                  # Run tests
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report
```

### Code Quality

#### Backend
```bash
# Linting
ruff check app/
ruff check --fix app/    # Auto-fix

# Type checking
mypy app/

# Format
ruff format app/
```

#### Frontend
```bash
# Linting
npm run lint

# Type checking
npm run type-check

# Format
npm run format  # If prettier configured
```

### Database Migrations

```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Show history
alembic history
```

### Adding Dependencies

#### Backend
```bash
cd backend
pip install new-package
pip freeze > requirements.txt  # Update requirements
```

#### Frontend
```bash
cd frontend
npm install new-package
# package.json and package-lock.json updated automatically
```

## IDE Configuration

### VS Code (Recommended)
Install extensions:
- Python
- Pylance
- Ruff
- TypeScript and JavaScript Language Features
- Tailwind CSS IntelliSense
- ES7+ React/Redux/React-Native snippets

Settings (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.ruff": "explicit",
    "source.organizeImports.ruff": "explicit"
  },
  "typescript.tsdk": "frontend/node_modules/typescript/lib"
}
```

## Project Structure

```
brand-gate/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities, API client
│   │   ├── hooks/           # Custom React hooks
│   │   └── types/           # TypeScript types
│   ├── public/              # Static assets
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── core/            # Config, security, database
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── db/              # Database utilities
│   │   └── utils/           # Helpers
│   ├── migrations/          # Alembic migrations
│   ├── tests/               # Test suite
│   ├── requirements.txt
│   └── alembic.ini
│
├── database/                 # Database schemas & sample data
│   ├── schema.sql
│   └── sample_data.sql
│
├── datasets/                 # Training/evaluation data
│   ├── brand_guidelines/
│   ├── approved_facts/
│   ├── brand_assets/
│   └── test_content/
│
├── docs/                     # Documentation
│   ├── architecture/
│   ├── api/
│   ├── development/
│   └── deployment/
│
├── scripts/                  # Utility scripts
│
├── tests/                    # End-to-end tests
│
├── .env.example
├── .gitignore
└── README.md
```

## Common Issues

### Database Connection Failed
- Ensure PostgreSQL is running: `docker ps` or `systemctl status postgresql`
- Check `DATABASE_URL` in `.env`
- Verify pgvector extension: `SELECT * FROM pg_extension WHERE extname = 'vector';`

### Ollama Connection Failed
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_BASE_URL` in `.env`
- Verify models pulled: `ollama list`

### Port Conflicts
- Frontend: 3000 (change in `package.json` or `PORT=3001 npm run dev`)
- Backend: 8000 (change in `uvicorn` command)
- Database: 5432
- Ollama: 11434

### Migration Errors
```bash
# Reset database (development only)
cd backend
alembic downgrade base
alembic upgrade head
```

## Useful Commands

```bash
# View logs
docker logs brand-gate-db

# Database shell
psql -h localhost -U postgres -d brand_gate

# Check API health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000
```

## Next Steps

1. Review [Architecture Documentation](../architecture/system_design.md)
2. Read [API Reference](../api/api_reference.md)
3. Check [Deployment Guide](../deployment/production.md)