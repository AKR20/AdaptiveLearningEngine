from fastapi import APIRouter
from app.core.constants import error_responses

chat = APIRouter(tags=["chat"],
                 responses=error_responses
                 )