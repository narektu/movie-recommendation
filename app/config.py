from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
   app_name: str = "Movie Recommendation API"
   database_url: str
   secret_key: str
   algorithm: str = "HS256"
   access_token_expire_minutes: int = 60

   class Config:
      env_file = ".env"

settings = Settings()