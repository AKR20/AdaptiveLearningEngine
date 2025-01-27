from fastapi import APIRouter
from app.core.constants import error_responses

analysis = APIRouter(tags=["analysis"],
                 responses=error_responses
                 )