from sqlalchemy import Column, Integer, String, Text, DateTime, func, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Movie(Base):
   __tablename__ = "movies"

   id = Column(Integer, primary_key=True, index=True)
   title = Column(String, index=True, nullable=False)
   release_year = Column(Integer, index=True, nullable=False)
   description = Column(Text, nullable=True) 
   genre = Column(String, nullable=True)

   average_rating = Column(Float, default=0.0)

   created_at = Column(DateTime(timezone=True), server_default=func.now())
   updated_at = Column(DateTime(timezone=True), onupdate=func.now())

   roatings = relationship("Rating", back_populates="movie")

   def __repr__(self):
      return f"<Movie(id={self.id}, title='{self.title}')"