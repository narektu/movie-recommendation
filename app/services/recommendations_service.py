from typing import List
from app.dependencies import DB_Session
from app.repositories.ratings_repo import RatingRepository
from app.repositories.movies_repo import MovieRepository
from app.ml.recommenders import collaborative_filtering_recommender, popularity_recommender
from app.schemas.movie import MovieOut
from app.config import settings

class RecommendationsService:

   @staticmethod
   async def get_collaborative_filtering_recs(db: DB_Session, user_id: int) -> List[MovieOut]:
      all_ratings = await RatingRepository.get_all_ratings(db)
      if not all_ratings:
         return []
      
      recommended_movie_ids = collaborative_filtering_recommender(target_user_id=user_id, all_ratings=all_ratings) # send the data to ML-func for getting films ID
      if not recommended_movie_ids:
         return []
      
      recommended_movies = await MovieRepository.get_movies_by_ids(db, recommended_movie_ids)
      return recommended_movies
   
   @staticmethod
   async def get_popularity_recs(db: DB_Session) -> List[MovieOut]:
      all_ratings = await RatingRepository.get_all_ratings(db)
      if not all_ratings:
         return []
      
      recommended_movie_ids = popularity_recommender(
         all_ratings=all_ratings,
         min_ratings=settings.popularity_min_ratings,
         top_n=settings.popularity_top_n
      )
      if not recommended_movie_ids:
         return []
      
      recommended_movies = await MovieRepository.get_movies_by_ids(db, recommended_movie_ids)
      return recommended_movies

