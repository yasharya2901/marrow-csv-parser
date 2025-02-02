from flask import Blueprint, request, jsonify
from app.services.movie_service import get_movies

movie_routes = Blueprint("movie_routes", __name__)

@movie_routes.route("/", methods=["GET"])
def list_movies():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 50))
    except ValueError:
        page = 1
        limit = 50

    year = request.args.get("year")
    language = request.args.get("language")
    sort_field = request.args.get("sort_field")
    sort_order = request.args.get("sort_order", "asc")

    movies = get_movies(page=page, limit=limit, year=year, language=language,
                        sort_field=sort_field, sort_order=sort_order)
    return jsonify(movies)
