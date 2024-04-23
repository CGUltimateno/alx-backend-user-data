#!/usr/bin/env python3
"""
Session authentication module
"""
import os
import uuid
from .auth import Auth
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Return a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def destroy_session(self, request=None):
        """
        Destroy a session
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True

    def session_cookie(self, request=None):
        """
        Return a session cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        User
        """
        if request:
            cookie = self.session_cookie(request)
            if cookie:
                user_id = self.user_id_for_session_id(cookie)
                return User.get(user_id)
