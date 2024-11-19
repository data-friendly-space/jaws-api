# user_management/repositories/user_repository.py
from abc import ABC

from user_management.contract.repository.base_repository import BaseRepository


class UserRepository(BaseRepository, ABC):
    """
    Interface for User repository with additional user-specific methods.
    """
    pass
