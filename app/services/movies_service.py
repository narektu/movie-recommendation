from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate

class MoviesService:
    @staticmethod
    async def get_movies(db: AsyncSession, skip: int = 0, limit: int = 10):
        query = select(Movie).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_movie(db: AsyncSession, movie_id: int):
        query = select(Movie).where(Movie.id == movie_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_movie(db: AsyncSession, movie_data: MovieCreate):
        movie = Movie(**movie_data.dict())
        db.add(movie)
        await db.commit()
        await db.refresh(movie)
        return movie

    @staticmethod
    async def update_movie(db: AsyncSession, movie_id: int, movie_data: MovieUpdate):
        query = select(Movie).where(Movie.id == movie_id)
        result = await db.execute(query)
        movie = result.scalar_one_or_none()
        if not movie:
            return None

        for key, value in movie_data.dict(exclude_unset=True).items():
            setattr(movie, key, value)

        await db.commit()
        await db.refresh(movie)
        return movie

    @staticmethod
    async def delete_movie(db: AsyncSession, movie_id: int):
        query = select(Movie).where(Movie.id == movie_id)
        result = await db.execute(query)
        movie = result.scalar_one_or_none()
        if not movie:
            return None

        await db.delete(movie)
        await db.commit()
        return movie
