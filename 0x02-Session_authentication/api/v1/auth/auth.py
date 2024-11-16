#!/usr/bin/env python3
"""
Authentication module for the API.
"""
import re
from typing import List, TypeVar
from flask import request, abort
from models.user import User


class Auth:
    """
    Auth class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        determines if a path requires authentication.
        """
        if path is None or not excluded_paths:
            return True

        if path[-1] != '/':
            path = path + '/'
        for pat in excluded_paths:
            if pat[-1] == '*':
                pat = pat[:-1] + '.*'
            if re.fullmatch(pat, path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets authorization header field from the request.
        """
        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            return authorization_header
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user from the request.
        """
        return None
