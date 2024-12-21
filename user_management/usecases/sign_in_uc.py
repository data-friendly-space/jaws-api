from common.use_case.base_use_case import BaseUseCase
from user_management.contract.repository.user_repository import UserRepository


class SignInUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if SignInUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SignInUC._instance = self

    @staticmethod
    def get_instance():
        if SignInUC._instance is None:
            SignInUC()
        return SignInUC._instance

    def exec(self, repository: UserRepository, data):
        return repository.sign_up(data)
