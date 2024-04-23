#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User

from typing import TypeVar


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None


    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session


    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to db
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(User)
        self.__session.commit()
        return user
    

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user with attributes
        """
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user
    
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates current user
        """
        user = user.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self.__session.add(user)
        self.__session.commit()