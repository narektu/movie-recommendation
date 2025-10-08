from fastapi import APIRouter
from . import users, movies, ratings, recommendations 

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
