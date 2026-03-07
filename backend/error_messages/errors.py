from flask import jsonify, make_response, request
from ..models.model_base.user_services.services import get_user_by_key
from functools import wraps 


def session_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("Checking Authorization using header method")
        token = request.headers.get('Authorization')
        if not token:
            print("Checking Authorization using json body method")
            data = request.get_json()
            token = data.get("session_key")  # Use .get() to avoid KeyError
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
        
        current_user = get_user_by_key(token.replace("Bearer ", ""))
        if not current_user:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(*args, **kwargs)  # Actually call the wrapped function
    return decorated


def ensure_requirements(requirements: list):
    """Decorator factory that validates required JSON fields"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.get_json()
            if not data:
                return NotFoundError("No JSON body provided").to_response()
            
            for item in requirements:
                if item not in data or not data[item]:
                    return NotFoundError(f'{item} not found in POST request').to_response()
            
            return f(*args, **kwargs)
        return decorated
    return decorator


def error(msg):
    return jsonify({'error': msg})


def error_response(message, status=400):
    payload = {'error': message}
    return make_response(jsonify(payload), status)


class Error(Exception):
    error_name = "Error"
    status = 500
    error_msg = ""

    def __init__(self, message=None):
        if message:
            self.error_msg = message

    def to_dict(self):
        return {
            'error_name': self.error_name,
            'status': self.status,
            'error_msg': self.error_msg,
        }

    def to_response(self):
        return make_response(jsonify(self.to_dict()), self.status)

    def add_error_message(self, message):
        self.error_msg = message
        return self


class BadRequestError(Error):
    error_name = "Bad Request"
    status = 400


class AuthenticationError(Error):
    error_name = "Authentication Error"
    status = 401


class AuthorizationError(Error):
    error_name = "Permission Error"
    status = 403


class NotFoundError(Error):
    error_name = "Not Found Error"
    status = 404


class ConflictError(Error):
    error_name = "Conflict Error"
    status = 409


class ValidationError(Error):
    error_name = "Validation Error"
    status = 422


class DatabaseError(Error):
    error_name = "Database Error"
    status = 500


class InternalServerError(Error):
    error_name = "Internal Server Error"
    status = 500


def to_response(err):
    """Convenience factory to convert exceptions or messages into Flask responses"""
    if isinstance(err, Error):
        return err.to_response()
    if isinstance(err, Exception):
        msg = str(err)
        return error_response(msg, 500)
    return error_response(str(err), 400)


__all__ = [
    'error',
    'error_response',
    'Error',
    'BadRequestError',
    'AuthenticationError',
    'AuthorizationError',
    'NotFoundError',
    'ConflictError',
    'ValidationError',
    'DatabaseError',
    'InternalServerError',
    'to_response',
    'session_key_required',
    'ensure_requirements',
]