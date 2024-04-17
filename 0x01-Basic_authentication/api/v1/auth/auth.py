#!/usr/bin/env python3
"""
Auth module
"""
from re import search, sub
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth"""
        if path is None or excluded_paths in ["", None]:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if (search(sub(r"\*", ".*", excluded_path), path)):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None