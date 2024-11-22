# user_management/repositories/user_repository.py
from abc import ABC, abstractmethod

from user_management.contract.repository.base_repository import BaseRepository


class UserRepository(BaseRepository, ABC):

    @abstractmethod
    def sign_up(self, name, lastname, email, password):
        pass

    @abstractmethod
    def get_user_by_email(self, email):
        pass
