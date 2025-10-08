from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingOut, RatingUpdate
from typing import List, Optional

class RatingRepository:
   
   @staticmethod
   async def get_rating_by_user_and_movie(db: AsyncSession, user_id: int, movie_id: int) -> Optional[Rating]:
      result = await db.execute(select(Rating).where(Rating.user_id == user_id, Rating.movie_id == movie_id))
      return result.scalar_one_or_none()
   
   @staticmethod
   async def get_ratings_by_user(db: AsyncSession, user_id: int) -> list[Rating]:
      result = await db.execute(select(Rating).where(Rating.user_id == user_id))
      return result.scalars().all()
   
   @staticmethod
   async def get_ratings_by_movie(db: AsyncSession, movie_id: int) -> list[Rating]:
      result = await db.execute(select(Rating).where(Rating.movie_id == movie_id))
      return result.scalars().all()
   
   @staticmethod
   async def create_rating(db: AsyncSession, rating_data: RatingCreate, user_id: int) -> Rating:
      new_rating = Rating(**rating_data.dict(), user_id=user_id)
      db.add(new_rating)
      await db.commit()
      await db.refresh(new_rating)
      return new_rating
   
   @staticmethod
   async def update_rating(db: AsyncSession, db_rating: Rating, rating_update: RatingUpdate) -> Rating:
      db_rating.score = rating_update.score
      db.add(db_rating)
      await db.commit()
      await db.refresh(db_rating)
      return db_rating

   @staticmethod
   async def get_all_ratings(db: AsyncSession) -> List[RatingOut]: 
      result = await db.execute(select(Rating))
      all_ratings = result.scalars().all()
      return [RatingOut.from_orm(rating) for rating in all_ratings]
   
   @staticmethod
   async def get_average_rating_for_movie(db: AsyncSession, movie_id: int) -> Optional[float]:
      query = select(func.avg(Rating.score)).where(Rating.movie_id == movie_id)
      result = await db.execute(query)
      avg_score = result.scalar()
      
      if avg_score is None:
         return None
         
      return round(avg_score, 2)