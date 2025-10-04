from typing import AsyncGenerator
from app.database import SessionLocal

async def get_db() -> AsyncGenerator:
   async with SessionLocal() as session:
      yield session
