from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.rating import RatingCreate, RatingUpdate
from app.repositories.ratings_repo import RatingRepository
from app.repositories.movies_repo import MovieRepository
from typing import Optional

class RatingsService:

    @staticmethod
    async def create_rating(db: AsyncSession, rating_in: RatingCreate, user_id: int):
        movie = await MovieRepository.get_movie_by_id(db, rating_in.movie_id)
        
        if not movie:
            raise ValueError("Movie with this ID does not exist")

        existing_rating = await RatingRepository.get_rating_by_user_and_movie(db, user_id=user_id, movie_id=rating_in.movie_id)
        
        if existing_rating:
            raise ValueError("You have already rated this movie. Use another option.")
        
        return await RatingRepository.create_rating(db=db, rating_data=rating_in, user_id=user_id)
    
    @staticmethod
    async def update_rating(db: AsyncSession, rating_update: RatingUpdate, user_id: int, movie_id: int):
        db_rating = await RatingRepository.get_rating_by_user_and_movie(db, user_id=user_id, movie_id=movie_id)

        if not db_rating:
            raise ValueError("You have not rated this movie yet. Use another option.")

        return await RatingRepository.update_rating(db=db, db_rating=db_rating, rating_update=rating_update)

    @staticmethod
    async def get_ratings_by_movie(db: AsyncSession, movie_id: int):
        return await RatingRepository.get_ratings_by_movie(db, movie_id=movie_id)

    @staticmethod
    async def get_ratings_by_user(db: AsyncSession, user_id: int):
        return await RatingRepository.get_ratings_by_user(db, user_id=user_id)

    @staticmethod
    async def get_average_rating(db: AsyncSession, movie_id: int) -> Optional[float]:
        return await RatingRepository.get_average_rating_for_movie(db, movie_id=movie_id)

