from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

# User Table
class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   email = Column(String, unique=True, index=True, nullable=False)
   hashed_password = Column(String, nullable=False)
   created_at = Column(DateTime(timezone=True), server_default=func.now())

   ratings = relationship("Rating", back_populates="user")
   
   def __repr__(self):
       return f"<User(id={self.id}, email='{self.email}')>"