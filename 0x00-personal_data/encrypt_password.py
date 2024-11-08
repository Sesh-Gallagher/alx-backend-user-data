#!/usr/bin/env python3
""" Encrypting passwords """
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Module that expects one string argument name password

    Returns:salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks whether the expected  argument (password)
    is valid and returns a boolean.
    Args: hashed_password (bytes): hashed password
          password (str): password in string

    Return:bool
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
