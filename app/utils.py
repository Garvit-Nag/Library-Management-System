from functools import wraps
from flask import request, jsonify, current_app
from typing import Callable, Any

def require_auth(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid token"}), 401

        token = auth_header.split(' ')[1]

        db = current_app.db

        user_id = db.validate_token(token)
        if user_id is None:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.user_id = user_id
        return func(*args, **kwargs)

    return wrapper
