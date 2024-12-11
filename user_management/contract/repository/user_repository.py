"""This module contains the implementation of user repository"""
from abc import ABC, abstractmethod

from common.repository.base_repository import BaseRepository


class UserRepository(BaseRepository, ABC):
    """User repository"""

    @abstractmethod
    def sign_up(self, name, lastname, email, password):
        """
        Create new user.
        """
        pass

    @abstractmethod
    def get_user_by_email(self, email):
        """
        Retrieve user from the database by email address.
        """
        pass

    @abstractmethod
    def get_user_by_filters(self, **kwargs):
        """
           Get users based on dynamic filters.
           Accepts any combination of filter arguments.
           """
        pass
