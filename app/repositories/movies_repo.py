from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate

class MovieRepository:

   @staticmethod
   async def get_movie_by_id(db: AsyncSession, movie_id: int) -> Movie | None:
      result = await db.execute(select(Movie).where(Movie.id == movie_id))
      return result.scalar_one_or_none()
   
   @staticmethod
   async def get_movies(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Movie]:
      result = await db.execute(select(Movie).offset(skip).limit(limit).order_by(Movie.id))
      return result.scalars().all()
   
   @staticmethod
   async def create_movie(db: AsyncSession, db_movie: Movie, movie_update: MovieUpdate) -> Movie:
      new_movie = Movie(**movie_in.dict())
      db.add(new_movie)
      await db.commit()
      await db.refresh(new_movie)
      return new_movie
   
   @staticmethod
   async def update_movie(db: AsyncSession, db_movie: Movie, movie_update: MovieUpdate) -> Movie:
      update_data = movie_update.dict(exclude_unset=True)

      for key, value in update_data.items():
         setattr(db_movie, key, value)

      await db.commit()
      await db.refresh(db_movie)
      return db_movie
   
   @staticmethod
   async def delete_movie(db: AsyncSession, movie: Movie) -> None:
      await db.delete(movie)
      await db.commit()