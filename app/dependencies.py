from typing import AsyncGenerator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.utils import security
from app.schemas.user import UserOut

async def get_db() -> AsyncGenerator[AsyncSession, None]:
   async with AsyncSessionLocal() as session:
      yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserOut:
   payload = security.decode_access_token(token)

   if payload is None:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Could not validate credentials",
         headers={"WWW-Authenticate": "Bearer"},
      )
   

   try:
      return UserOut(id=1, email="authenticated_user@example.com")
   except Exception as e:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Token payload is invalid",
         headers={"WWW-Authenticate": "Bearer"},
      )
   
CurrentUser = Annotated[UserOut, Depends(get_current_user)],
DB_Session = Annotated[AsyncSession, Depends(get_db)]
