'''This module contains the user service'''
from abc import ABC, abstractmethod


class UsersService(ABC):
    '''User service'''
    @abstractmethod
    def get_users(self):
        '''Retrieves the users'''

    @abstractmethod
    def sign_up(self, name, lastname, email, password):
        '''Create a new user'''

    @abstractmethod
    def sign_in(self, email, password):
        '''Log-in a user'''

    @abstractmethod
    def refresh_token(self, refresh_token):
        '''Refresh the user's token'''
    @abstractmethod
    def verify_token(self, auth_header):
        '''Validate the user's token'''
