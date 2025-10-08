from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.rating import RatingCreate, RatingOut, RatingUpdate
from app.services.ratings_service import RatingsService
from app.dependencies import DB_Session, CurrentUser
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

@router.post("/", response_model=RatingOut, status_code=status.HTTP_201_CREATED)
async def create_rating(rating_in: RatingCreate, db: DB_Session, current_user: CurrentUser):
   try:
      return await RatingsService.create_rating(db, rating_in=rating_in, user_id=current_user.id)
   except ValueError as e:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/movie/{movie_id}", response_model=List[RatingOut])
async def get_ratings_for_movie(movie_id: int, db: DB_Session):
   return await RatingsService.get_ratings_by_movie(db, movie_id)

@router.get("/my-ratings", response_model=List[RatingOut])
async def get_my_ratings(db: DB_Session, current_user: CurrentUser):
   user_id = current_user.id
   return await RatingsService.get_ratings_by_user(db, user_id)

@router.put("/movie/{movie_id}", response_model=RatingOut)
async def update_rating(movie_id: int, rating_update: RatingUpdate, db: DB_Session, current_user: CurrentUser):
   try:
      return await RatingsService.update_rating(db, rating_update=rating_update, user_id=current_user.id, movie_id=movie_id)
   except ValueError as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
   
# @router.get("/movie/{movie_id}/average-rating", response_model=RatingAverageResponse) --> RatingAverageResponse planned
# async def get_movie_average_rating(movie_id: int, db: DB_Session):
#     avg_rating = await RatingsService.get_average_rating(db, movie_id)
#     return RatingAverageResponse(movie_id=movie_id, average_rating=avg_rating)