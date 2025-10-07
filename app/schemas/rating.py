from pydantic import BaseModel, Field
from typing import Optional
from .movie import MovieOut
from datetime import datetime


class RatingBase(BaseModel):
   score: float = Field(..., ge=0.5, le=5.0) 

class RatingCreate(RatingBase):
   movie_id: int 

class RatingOut(RatingBase):
   id: int
   user_id: int       
   movie_id: int         
   created_at: datetime
   
   class Config:
      orm_mode = True


class RatingMovieOut(RatingOut):
   movie: MovieOut