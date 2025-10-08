from fastapi import APIRouter, Depends
from typing import List
from app.dependencies import DB_Session, CurrentUser
from app.services.recommendations_service import RecommendationsService
from app.schemas.movie import MovieOut

router = APIRouter()

@router.get("/me", response_model=List[MovieOut])
async def get_my_recommendations(db: DB_Session, current_user: CurrentUser):
   recommendations = await RecommendationsService.get_collaborative_filtering_recs(db=db, user_id=current_user.id)
   return recommendations

@router.get("/popular", response_model=List[MovieOut])
async def get_popular_movies(db: DB_Session):
   return await RecommendationsService.get_popularity_recs(db=db)
