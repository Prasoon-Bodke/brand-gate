from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, guidelines, facts, assets, submissions, findings, reviews, approvals

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(guidelines.router, prefix="/guidelines", tags=["guidelines"])
api_router.include_router(facts.router, prefix="/facts", tags=["facts"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
api_router.include_router(findings.router, prefix="/findings", tags=["findings"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["approvals"])