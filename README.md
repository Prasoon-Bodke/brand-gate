# Brand Gate

### Catch off-brand content before it goes live.

Brand Gate is an AI-powered brand governance platform that reviews posts, advertisements, images and documents against an organisation's approved brand guidelines, facts and visual assets.

It detects brand inconsistencies, explains every issue with supporting evidence and suggests corrections while keeping humans in control of the final approval.

## Problem

Organisations publish content through employees, external agencies and AI tools. Maintaining consistent brand identity across all these sources is difficult.

Brand Gate helps prevent:
- Unsupported promotional claims.
- Outdated company information.
- Inconsistent brand terminology and tone.
- Incorrect logo and colour usage.
- Accessibility issues.
- Unclear and inconsistent review decisions.

## Core Features

- Brand Knowledge Base
- Approved Facts and Claims Ledger
- Multi-format Content Review
- Evidence-backed AI Findings
- Intelligent Correction Suggestions
- Human Review and Approval Workflow
- Content Version History
- Brand Governance Analytics
- Confidential Content Processing

## AI Checking Pipeline

Brand Gate uses three checking tiers:

**Tier 0 — Deterministic Rules**
- Banned and outdated terminology.
- Claim-word detection.
- Readability checks.
- Brand colour and font checks.
- Accessibility and contrast checks.

**Tier 1 — Jev Decision Model**
- Brand tone analysis.
- Contextual rule evaluation.
- Structured classification.
- Confidence-based decisions.

**Tier 2 — Open-weight LLM**
- Explain detected issues.
- Generate minimal corrections.
- Preserve original meaning.
- Recheck suggested corrections.

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, TypeScript |
| Styling | Tailwind CSS |
| Backend | FastAPI, Python |
| Database | PostgreSQL, Supabase |
| Vector Search | pgvector |
| Decision Model | Jev by TypeSafe AI |
| LLM | Qwen / Llama |
| Model Integration | LiteLLM |
| Document Processing | Docling |
| OCR | PaddleOCR |
| Image Matching | SigLIP |
| Local Inference | Ollama |

## User Roles

1. Brand Admin
2. Creator
3. Reviewer
4. Approver

## Project Architecture

```text
Next.js Frontend
       |
       v
FastAPI Backend
       |
       v
Content Processing
       |
       v
Three-Tier AI Pipeline
       |
       v
Evidence-backed Findings
       |
       v
Correction and Self-check
       |
       v
Human Review and Approval
       |
       v
Governance Analytics
```

## Project Structure

```text
brand-gate/
├── frontend/
├── backend/
├── database/
├── datasets/
├── docs/
├── scripts/
├── README.md
└── .env.example
```

## Development Team

| Member | Role |
|---|---|
| Jiteesh Ghodke | AI / ML |
| Prasoon Bodke | Backend |
| Advait Malwade | Frontend |
| Samiksha Bhusare | Product / Research / Presentation |

## Development Status

Project developed as part of CodeNexus India 2026.

## Responsible AI

- AI suggestions are never applied automatically.
- Humans retain final approval authority.
- Uncertain findings are escalated for human review.
- Confidential content is processed locally.
- AI services used for each review are disclosed.

## License

To be finalised by the project team.
