from abc import ABC, abstractmethod


class UsersService(ABC):
    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def sign_up(self, name, lastname, email, password):
        pass

    @abstractmethod
    def sign_in(self, email, password):
        pass

    @abstractmethod
    def refresh_token(self, refresh_token):
        pass
    @abstractmethod
    def verify_token(self, auth_header):
        pass
