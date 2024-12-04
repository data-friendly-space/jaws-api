'''This module contains the get user by id use case'''


class GetUserByEmailUC:
    '''Retrieve a user based on a given email'''
    _instance = None

    def __init__(self):
        if GetUserByEmailUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUserByEmailUC._instance = self

    @staticmethod
    def get_instance():
        '''Retrieve a single instance of the class'''
        if GetUserByEmailUC._instance is None:
            GetUserByEmailUC()
        return GetUserByEmailUC._instance

    def exec(self, repository, email):
        '''Execute the use case'''
        return repository.get_user_by_email(email)
