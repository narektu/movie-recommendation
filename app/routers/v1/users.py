from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserOut
from app.services.users_service import UserService
from app.repositories.users_repo import UsersRepository
from app.dependencies import CurrentUser, DB_Session
from app.utils import security


router = APIRouter()

@router.post("/", response_model=UserOut)
async def register_user(user_in: UserCreate, db: DB_Session):
   try:
      return await UserService.register_user(db, user_in)
   except ValueError as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
   
@router.get("/", response_model=list[UserOut])
async def list_users(db: DB_Session):
   return await UserService.list_users(db)

@router.post("/login", response_model=security.Token)
async def login(db: DB_Session, form_data: OAuth2PasswordRequestForm = Depends()):
   user = await UsersRepository.get_user_by_email(db, form_data.username)
   if not user or not security.verify_password(form_data.password, user.hashed_password):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password", headers={"WWW-Authenticate": "Bearer"})
   access_token = security.create_access_token(data={"sub": user.email})
   return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: CurrentUser):
    return current_user