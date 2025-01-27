from fastapi import APIRouter
from app.core.constants import error_responses
from app.session.endpoints import session_router
from app.chatWithLearner.endpoints import chat
from app.analysis.endpoints import analysis

core_router = APIRouter(prefix="",
                        responses=error_responses
                        )

core_router.include_router(session_router)
core_router.include_router(chat)
core_router.include_router(analysis)