from fastapi import FastAPI
from app.config import settings
from app.routers.v1 import __init__ as v1_router
from app.logging_config import logger

app = FastAPI(title=settings.app_name, version="1.0")

app.include_router(v1_router.router, prefix="/api/v1")

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to Movie Recommendation API"}
