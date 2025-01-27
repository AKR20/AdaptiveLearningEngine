from fastapi import APIRouter
from app.core.constants import error_responses

session_router = APIRouter(tags=["session_router"],
                 responses=error_responses
                 )