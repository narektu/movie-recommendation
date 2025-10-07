from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.logging_config import logger
from app.routers.v1 import router as v1_router
from app.database import engine, Base

app = FastAPI(title=settings.app_name, version="1.0")

app.include_router(v1_router, prefix="/api/v1")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to Movie Recommendation API"}

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)