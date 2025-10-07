from typing import AsyncGenerator
from app.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator:
   async with AsyncSessionLocal() as session:
      yield session
