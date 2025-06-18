from flask import request
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per day", "30 per hour"]
)

def rate_limit(limit_string="10 per minute"):
    def decorator(f):
        @wraps(f)
        @limiter.limit(limit_string)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped
    return decorator