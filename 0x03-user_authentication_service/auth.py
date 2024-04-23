#!/usr/bin/env python3
"""
Authentication Module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from db import DB, User

def _hash_password(password: str) -> bytes:
    """
    Encrypts a password
    """
    return bcrypt.hashpw