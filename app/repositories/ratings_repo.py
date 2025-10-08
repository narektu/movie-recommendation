from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingOut
from typing import List

class RatingRepository:
   
   @staticmethod
   async def get_ratina_by_id(db: AsyncSession, rating_id: int) -> Rating | None:
      result = await db.execute(select(Rating).where(Rating.id == rating_id))
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
   async def create_rating(db: AsyncSession, rating_in: RatingCreate, user_id: int) -> Rating:
      rating_data = rating_in.dict()
      rating_data["user_id"] = user_id

      new_rating = Rating(**rating_data)
      db.add(new_rating)
      await db.commit()
      await db.refresh(new_rating)
      return new_rating

   @staticmethod
   async def get_all_ratings(db: AsyncSession) -> List[RatingOut]: 
      result = await db.execute(select(Rating))
      all_ratings = result.scalars().all()
      return [RatingOut.from_orm(rating) for rating in all_ratings]