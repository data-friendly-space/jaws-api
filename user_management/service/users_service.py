from abc import ABC, abstractmethod


class UsersService(ABC):
    @abstractmethod
    def get_users(self):
        pass
