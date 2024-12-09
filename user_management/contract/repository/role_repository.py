'''This module contains the role repository'''
from abc import ABC, abstractmethod

from common.repository.base_repository import BaseRepository


class RoleRepository(BaseRepository, ABC):
    '''Role repository'''
    @abstractmethod
    def get_roles(self, exclusions):
        pass

