#!/usr/bin/env python3
"""
BasicAuth module
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from base64 import b64decode
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract base64 authorization header"""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decode base64 authorization header"""
        if base64_authorization_header is None or type(base64_authorization_header) is not str:
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials"""
        if decoded_base64_authorization_header is None or type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """User object from credentials"""
        if user_email is None or isinstance(user_email, str) is False:
            return None

        if user_pwd is None or isinstance(user_pwd, str) is False:
            return None

        list_of_users = []
        try:
            list_of_users = User.search({"email": user_email})
        except KeyError:
            return None
        user = None
        if len(list_of_users) == 0:
            return (None)
        user = list_of_users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        auth = self.authorization_header(request)
        auth_as_base_64 = self.extract_base64_authorization_header(auth)
        decoded_auth = self.decode_base64_authorization_header(auth_as_base_64)
        email, passwd = self.extract_user_credentials(decoded_auth)
        user = self.user_object_from_credentials(email, passwd)
        return user
