from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.movie import MovieCreate, MovieOut, MovieUpdate
from app.services.movies_service import MoviesService
from app.dependencies import DB_Session, CurrentUser
from typing import List

router = APIRouter()

@router.post("/", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
async def create_movie(movie_in: MovieCreate, db: DB_Session, current_user: CurrentUser):
   return await MoviesService.create_movie(db, movie_in)

@router.get("/", response_model=List[MovieOut])
async def list_movies(db: DB_Session, skip: int = 0, limit: int = 100):
   return await MoviesService.get_movies(db, skip=skip, limit=limit)

@router.get("/{movie_id}", response_model=MovieOut)
async def get_movie(movie_id: int, db: DB_Session):
   movie = await MoviesService.get_movie(db, movie_id)
   if not movie:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
   return movie

@router.put("/{movie_id}", response_model=MovieOut)
async def update_movie(movie_id: int, movie_in: MovieUpdate, db: DB_Session, current_user: CurrentUser):
   movie = await MoviesService.update_movie(db, movie_id, movie_in)
   if not movie:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
   return movie

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int, db: DB_Session, current_user: CurrentUser):
    success = await MoviesService.delete_movie(db, movie_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return None