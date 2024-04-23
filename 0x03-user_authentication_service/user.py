#!/usr/bin/env python3
"""
Authentication User Class
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    Authentication User Class
    """
    __tablename__ = 'users'

    id = Column(Integer, autoincrement="auto", primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))