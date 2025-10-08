from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.rating import RatingCreate, RatingOut
from app.services.ratings_service import RatingsService
from app.dependencies import DB_Session, CurrentUser
from typing import List

router = APIRouter()

@router.post("/", response_model=RatingOut, status_code=status.HTTP_201_CREATED)
async def create_or_update_rating(rating_in: RatingCreate, db: DB_Session, current_user: CurrentUser):
   try:
      user_id = current_user.id
      return await RatingsService.create_or_update_rating(db, rating_in, user_id)
   except ValueError as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/movie/{movie_id}", response_model=List[RatingOut])
async def get_ratings_for_movie(movie_id: int, db: DB_Session):
   return await RatingsService.get_ratings_by_movie(db, movie_id)

@router.get("/my-ratings", response_model=List[RatingOut])
async def get_my_ratings(db: DB_Session, current_user: CurrentUser):
   user_id = current_user.id
   return await RatingsService.get_ratings_by_user(db, user_id)