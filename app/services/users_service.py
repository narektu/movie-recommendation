from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.users_repo import UsersRepository
from app.schemas.user import UserCreate

class UserService:

   @staticmethod
   async def register_user(db: AsyncSession, user_in: UserCreate):
      existing = await UsersRepository.get_user_by_email(db, user_in.email)
      if existing:
         raise ValueError("User already exists")
      return await UsersRepository.create_user(db, user_in.email, user_in.password)
   
   @staticmethod
   async def list_users(db: AsyncSession):
      return await UsersRepository.get_users(db)