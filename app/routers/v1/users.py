from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut
from app.services.users_service import UsersService
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
   try:
      return await UsersService.register_user(db, user_in)
   except ValueError as e:
      raise HTTPException(status_code=400, detail=str(e))
   
@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
   return await UsersService.list_users(db)