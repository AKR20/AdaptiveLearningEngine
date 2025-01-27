from fastapi import FastAPI
from app.core.custom_logger import CustomLogger
from app.core.routers import core_router

logger = CustomLogger()

# Initialize FastAPI app
app = FastAPI(title="Adaptive Learning Engine", version="1.0")

@app.get("/")
def root():
    """Root endpoint to check API health."""
    return {"message": "Adaptive Learning Engine API is running"}

app.include_router(core_router)