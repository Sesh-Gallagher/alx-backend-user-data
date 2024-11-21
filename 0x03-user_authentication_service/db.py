#!/usr/bin/env python3
""" Represents the  Database for ORM """
from sqlalchemy import create_engine, tuple_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar, Type, Mapping, Dict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt

from user import Base, User


class DB:
    """
    DB class module
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Module that adds a User to db
        and Returns a User object
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Module to Find a user based on a set of filters.
        """
        values, fields = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        results = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if results is None:
            raise NoResultFound()
        return results

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Uses find_user_by to locate a user based on a given id.
        """
        new_user = self.find_user_by(id=user_id)
        if new_user is None:
            return
        updated_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                updated_source[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            update_source,
            synchronize_session=False,
        )
        self._session.commit()
