from app.models.base_model import BaseModel
from datetime import datetime
from pydantic import BaseModel as PydanticModel, Field
from typing import List, Optional

class MovieSchema(PydanticModel):
    """Schema for validating movie data before insertion."""
    budget: Optional[int] = Field(None, ge=0, description="Movie budget in USD")
    homepage: Optional[str] = Field(None, description="Official website URL")
    original_language: str = Field(..., description="Original language of the movie")
    original_title: str = Field(..., description="Original title")
    overview: Optional[str] = Field(None, description="Brief description")
    release_date: datetime = Field(..., description="Release date in YYYY-MM-DD format")
    revenue: Optional[int] = Field(None, ge=0, description="Revenue in USD")
    runtime: Optional[int] = Field(None, ge=0, description="Movie duration in minutes")
    status: str = Field(..., description="Production status (e.g., Released, Upcoming)")
    title: str = Field(..., description="Movie title")
    vote_average: Optional[float] = Field(0.0, ge=0, le=10, description="Average user rating")
    vote_count: Optional[int] = Field(0, ge=0, description="Total number of votes")
    production_company_id: Optional[List[int]] = Field(None, description="List of production company IDs")
    genre_id: Optional[List[int]] = Field(None, description="List of genre IDs")
    languages: Optional[List[str]] = Field(None, description="List of available languages")

    class Config:
        from_attributes = True

class MovieModel(BaseModel):
    collection_name = "movies"

    @classmethod
    def insert_movie(cls, movie_data: dict):
        """Validates and inserts a movie record into MongoDB."""
        try:
            movie = MovieSchema(**movie_data)
            return cls.insert_one(movie.model_dump())
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def insert_movies(cls, movies: List[dict]):
        """Validates and inserts multiple movies into MongoDB."""
        try:
            validated_movies = [MovieSchema(**movie).model_dump() for movie in movies]
            return cls.insert_many(validated_movies)
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def find_movies(cls, query={}, limit=50):
        """Fetch movies with optional filtering."""
        return cls.find_all(query, limit)
