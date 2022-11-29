from flask import jsonify


def setup_error_template(app):
    """
    Error handling
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": f"Not found: {error.description}",
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": f"Data is Unprocessable : {error.description}"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": f"Bad request: {error.description}",
            "error_name": f"{error}"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": f"Internal server error: {error.description}",
        }), 500

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": f"Unauthorized: {error.description}",
        }), 401