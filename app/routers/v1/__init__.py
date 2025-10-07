# app/routers/v1/__init__.py
from fastapi import APIRouter
from .users import router as users_router
# from .movies import router as movies_router
# from .ratings import router as ratings_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
# api_router.include_router(movies_router, prefix="/movies", tags=["movies"])
# api_router.include_router(ratings_router, prefix="/ratings", tags=["ratings"])
