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

    @abstractmethod
    def get_user_by_email(self, email):
        """
        Retrieve user from the database by email address.
        """

    @abstractmethod
    def get_user_by_filters(self, **kwargs):
        """
           Get users based on dynamic filters.
           Accepts any combination of filter arguments.
           """

    @abstractmethod
    def is_user_in_analysis(self, user_id: str, analysis_id: int) -> bool:
        """Verify if an user belongs to an analysis 
        
        Keyword arguments:
        user_id -- the id of the user
        analysis_id -- the id of the analysis
        Return: True if the user belongs and False if not
        """
