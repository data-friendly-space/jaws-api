"""This module contains the sign up use case"""
class SignUpUC:
    """Class for handling the sign up process"""
    _instance = None

    def __init__(self):
        if SignUpUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SignUpUC._instance = self

    @staticmethod
    def get_instance():
        """Returns an instance of the class"""
        if SignUpUC._instance is None:
            SignUpUC()
        return SignUpUC._instance

    def exec(self, repository, name, lastname, email, password):
        """Execute de use case"""
        return repository.sign_up(name, lastname, email, password)
