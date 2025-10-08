from typing import List
from app.dependencies import DB_Session
from app.repositories.ratings_repo import RatingRepository
from app.repositories.movies_repo import MovieRepository
from app.ml.recommenders import collaborative_filtering_recommender
from app.schemas.movie import MovieOut

class RecommendationsService:

   @staticmethod
   async def get_collaborative_filtering_recs(db: DB_Session, user_id: int) -> List[MovieOut]:
      all_ratings = await RatingRepository.get_all_ratings(db)
      if not all_ratings:
         return []
      
      recommended_movie_ids = collaborative_filtering_recommender(target_user_id=user_id, all_ratings=all_ratings) # send the data to ML-func for getting films ID
      if not recommended_movie_ids:
         return []
      
      recommended_movie = await MovieRepository.get_movie_by_id(db, recommended_movie_ids)
      return recommended_movie