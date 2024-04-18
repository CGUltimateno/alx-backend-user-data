#!/usr/bin/env python3
"""
Auth module
"""
import os
from re import search, sub
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def __init__(self):
        """Constructor"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth"""
        if not path:
            return True
        if not excluded_paths:
            return True
        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None

    def session_cookie(self, request=None):
        """ Return a session cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
