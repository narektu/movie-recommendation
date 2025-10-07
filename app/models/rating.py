from sqlalchemy import Column, Integer, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")

    def __repr__(self):
        return f"<Rating(id={self.id}, user_id={self.user_id}, movie_id={self.movie_id}, score={self.score})>"
