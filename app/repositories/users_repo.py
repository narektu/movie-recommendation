from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from app.models.user import User
from app.utils.security import get_password_hash

class UsersRepository:

   @staticmethod
   async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
      result = await db.execute(select(User).where(User.email == email))
      return result.scalar_one_or_none()
   
   @staticmethod
   async def create_user(db: AsyncSession, email: str, password: str) -> User:
      hashed_pw = get_password_hash(password)
      new_user = User(email=email, hashed_password=hashed_pw)
      db.add(new_user)
      await db.commit()
      await db.refresh(new_user)
      return new_user
   
   @staticmethod
   async def get_users(db: AsyncSession) -> list[User]:
      result = await db.execute(select(User))
      return result.scalars().all()