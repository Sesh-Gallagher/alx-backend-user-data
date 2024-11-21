#!/usr/bin/env python3
"""
Module used for  authentication-related routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Takes in password string argument
    Returns bytes (salted_hashed).
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Returns string repr of a new UUID
    Use uuid module
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initializes a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Takes mandatory string (email, password) arguments
        Returns a User object
        Raise ValueError if exists
        User <user's email> already exists
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))
