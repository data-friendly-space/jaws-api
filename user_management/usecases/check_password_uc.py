"""This module the use case for checking a password"""
from user_management.repository.user_repository import UserRepository


class CheckPasswordUC:
    """Check that the password is correct"""
    _instance = None

    def __init__(self):
        if CheckPasswordUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CheckPasswordUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if CheckPasswordUC._instance is None:
            CheckPasswordUC()
        return CheckPasswordUC._instance

    def exec(self, repository: UserRepository, user_id: str, password: str) -> bool:
        """Execute the use case"""
        return repository.check_password(user_id, password)
