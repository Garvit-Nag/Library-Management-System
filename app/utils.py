from functools import wraps
from flask import request, jsonify, current_app
from typing import Callable, Any

def require_auth(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Get the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid token"}), 401

        # Extract the token
        token = auth_header.split(' ')[1]

        # Access the shared database instance
        db = current_app.db

        # Validate the token
        user_id = db.validate_token(token)
        if user_id is None:
            return jsonify({"error": "Invalid or expired token"}), 401

        # Add user_id to the request context
        request.user_id = user_id
        return func(*args, **kwargs)

    return wrapper