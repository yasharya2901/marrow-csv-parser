from datetime import datetime
from bson import ObjectId
from app.models.movie_model import MovieModel

def get_movies(page=1, limit=50, year=None, language=None, sort_field=None, sort_order="asc"):
    """
    Returns a list of movies from MongoDB with pagination, filtering, and sorting.

    Parameters:
      - page: which page number (default 1)
      - limit: number of items per page (default 50)
      - year: filter movies released in a given year (as an integer or string)
      - language: filter movies by their original language (e.g., "en")
      - sort_field: field to sort by ("release_date" or "rating")
      - sort_order: "asc" for ascending or "desc" for descending order

    Returns:
      - List of movie documents.
    """
    query = {}

    if year:
        try:
            year_int = int(year)
            start = datetime(year_int, 1, 1)
            end = datetime(year_int + 1, 1, 1)
            query["release_date"] = {"$gte": start, "$lt": end}
        except ValueError:
            pass

    if language:
        query["original_language"] = language

    skip = (page - 1) * limit

    sort = None
    if sort_field:
        if sort_field == "release_date":
            field = "release_date"
        elif sort_field == "rating":
            field = "vote_average"
        else:
            field = sort_field
        order = 1 if sort_order.lower() == "asc" else -1
        sort = [(field, order)]

    col = MovieModel.collection()
    cursor = col.find(query)

    if sort:
        cursor = cursor.sort(sort)
    if skip:
        cursor = cursor.skip(skip)
    if limit:
        cursor = cursor.limit(limit)

    movies = list(cursor)
    for movie in movies:
        if "_id" in movie:
            movie["_id"] = str(movie["_id"])

    return movies

def get_movie_by_id(movie_id):
    """
    Returns a single movie by its MongoDB ObjectId.

    Parameters:
      - movie_id: the string representation of the MongoDB _id

    Returns:
      - Movie document or None if not found
    """
    try:
        col = MovieModel.collection()
        movie = col.find_one({"_id": ObjectId(movie_id)})
        if movie:
            movie["_id"] = str(movie["_id"])
        return movie
    except Exception as e:
        print(f"Error fetching movie by ID: {e}")
        return None
