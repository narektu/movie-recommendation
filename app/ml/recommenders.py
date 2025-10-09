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

def popularity_recommender(all_ratings: List[RatingOut], min_ratings: int, top_n: int) -> List[int]:
   if not all_ratings:
      return[]
   
   df = pd.DataFrame([r.dict() for r in all_ratings])

   movie_stats = df.groupby('movie_id')['score'].agg(['count', 'mean']).reset_index()
   movie_stats = movie_stats.rename(columns={'count': 'num_ratings', 'mean': 'avg_rating'})

   global_avg_rating = df['score'].mean()

   qualified_movies = movie_stats[movie_stats['num_ratings'] >= min_ratings]

   if qualified_movies.empty:
      return[]
   
   # Calculate the weighted score for each qualified movie
   v = qualified_movies['num_ratings']
   m = min_ratings
   R = qualified_movies['avg_rating']
   C = global_avg_rating
   
   qualified_movies['weighted_score'] = (v / (v + m)) * R + (m / (v + m)) * C
   
   top_movies = qualified_movies.sort_values('weighted_score', ascending=False).head(top_n)
   return top_movies['movie_id'].tolist()


