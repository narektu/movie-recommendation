import pandas as pd
from app.schemas.rating import RatingOut
from typing import List

def collaborative_filtering_recommender(target_user_id: int, all_ratings: List[RatingOut]) -> List[int]:
   ratings_data = [r.dict() for r in all_ratings]
   if not ratings_data:
      return []
   
   df = pd.DataFrame(ratings_data)

   user_movie_matrix = df.pivot_table(index='user_id', columns='movie_id', values='score')
   user_correlation = user_movie_matrix.T.corr()

   if target_user_id not in user_correlation:
      return []
   
   similar_users = user_correlation[target_user_id].drop(target_user_id).sort_values(ascending=False)
   similar_users = similar_users.head(5)

   recommendations = set()
   seen_movies = user_movie_matrix.loc[target_user_id].dropna().index.tolist()

   for user_id, score in similar_users.items():
      if score > 0.5:
         liked_movies = user_movie_matrix.loc[user_id]
         liked_movies = liked_movies[liked_movies > 3].dropna().index.tolist() # ?

         for movie_id in liked_movies:
            if movie_id not in seen_movies:
               recommendations.add(movie_id)
   
   return list(recommendations)

