from flask import jsonify

class APIError(Exception):
    """Custom API Exception for structured error responses."""
    def __init__(self, message, status_code):
        super().__init__()
        self.message = message
        self.status_code = status_code

def error_response(message, status_code=400):
    """Returns a standard error response."""
    return jsonify({"error": message}), status_code

def register_error_handlers(app):
    """Register custom error handlers with the Flask app."""
    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({"error": "Bad Request", "message": str(error)})
        response.status_code = 400
        return response

    @app.errorhandler(404)
    def not_found(error):
        response = jsonify({"error": "Not Found", "message": str(error)})
        response.status_code = 404
        return response

    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify({"error": "Internal Server Error", "message": str(error)})
        response.status_code = 500
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all other exceptions."""
        response = jsonify({"error": "An unexpected error occurred", "message": str(error)})
        response.status_code = 500
        return response