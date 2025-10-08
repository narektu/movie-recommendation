from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.rating import Rating
from app.schemas.rating import RatingCreate

class RatingsService:
    @staticmethod
    async def create_or_update_rating(db: AsyncSession, rating_data: RatingCreate, user_id: int):
        query = select(Rating).where(
            Rating.user_id == user_id,
            Rating.movie_id == rating_data.movie_id
        )
        result = await db.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            existing.score = rating_data.score
            await db.commit()
            await db.refresh(existing)
            return existing

        rating = Rating(user_id=user_id, **rating_data.dict())
        db.add(rating)
        await db.commit()
        await db.refresh(rating)
        return rating

    @staticmethod
    async def get_movie_ratings(db: AsyncSession, movie_id: int):
        query = select(Rating).where(Rating.movie_id == movie_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_user_ratings(db: AsyncSession, user_id: int):
        query = select(Rating).where(Rating.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_average_rating(db: AsyncSession, movie_id: int):
        query = select(func.avg(Rating.score)).where(Rating.movie_id == movie_id)
        result = await db.execute(query)
        avg = result.scalar()
        return round(avg, 2) if avg else None
