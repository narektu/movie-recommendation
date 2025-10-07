from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MovieBase(BaseModel):
   title: str = Field(..., min_length=1, max_length=255)
   release_year: int = Field(..., gt=1915, lt=2025)
   description: Optional[str] = None
   genre: Optional[str] = None

class MovieCreate(MovieBase): # MovieBase exists
   pass

class MovieUpdate(MovieBase):
   title: Optional[str] = None
   release_year: Optional[int] = None

class MovieOut(MovieBase):
   id: int
   created_at: datetime
   updated_at: Optional[datetime]

   class Config:
      orm_mode = True
