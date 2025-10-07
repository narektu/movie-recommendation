from fastapi import FastAPI
from app.config import settings
from app.logging_config import logger
from app.routers.v1 import api_router
from app.database import engine, Base

app = FastAPI(
    title=settings.app_name,
    version="1.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to Movie Recommendation API"}
