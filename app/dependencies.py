from typing import AsyncGenerator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.utils import security
from app.schemas.user import UserOut
from app.repositories.users_repo import UsersRepository

async def get_db() -> AsyncGenerator[AsyncSession, None]:
   async with AsyncSessionLocal() as session:
      yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
DB_Session = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DB_Session) -> UserOut:
   payload = security.decode_access_token(token)

   if not payload or "sub" not in payload:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Could not validate credentials",
         headers={"WWW-Authenticate": "Bearer"},
      )
   
   email: str = payload.get("sub")
   user = await UsersRepository.get_user_by_email(db, email)

   if user is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="User not found",
      )
   return UserOut.from_orm(user)
   
CurrentUser = Annotated[UserOut, Depends(get_current_user)]
