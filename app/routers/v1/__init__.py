from fastapi import APIRouter
from . import users_router, movies_router, ratings_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(movies_router, prefix="/movies", tags=["movies"])
api_router.include_router(ratings_router, prefix="/ratings", tags=["ratings"])
