from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut
from app.services.users_service import UserService
from app.repositories.users_repo import UsersRepository
from app.dependencies import get_db
from app.utils import security
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(
      token: str = Depends(oauth2_scheme),
      db: AsyncSession = Depends(get_db)
) -> User:
   payload = security.decode.access_token(token)
   if not payload or "sub" not in payload:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Invalid credentials"
      )
   email = payload["sub"]
   user = await UsersRepository.get_user_by_email(db, email)
   if not user:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
   return user

@router.post("/", response_model=UserOut)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
   try:
      return await UserService.register_user(db, user_in)
   except ValueError as e:
      raise HTTPException(status_code=400, detail=str(e))
   
@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
   return await UserService.list_users(db)

@router.post("/login", response_model=security.Token)
async def login(
   form_data: OAuth2PasswordRequestForm = Depends(),
   db: AsyncSession = Depends(get_db)
):
   user = await UsersRepository.get_user_by_email(db, form_data.username)
   if not user or not security.verify_password(form_data.password, user.hashed_password):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
   access_token = security.create_access_token(data={"sub": user.email})
   return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user = await UsersService.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user