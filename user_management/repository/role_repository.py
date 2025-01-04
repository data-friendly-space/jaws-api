'''This module contains the role repository'''
from abc import ABC, abstractmethod

from common.repository.base_repository import BaseRepository
from user_management.contract.to.role_to import RoleTO


class RoleRepository(BaseRepository, ABC):
    '''Role repository'''

    @abstractmethod
    def get_roles(self, exclusions):
        """Retrieve all roles"""
        

    @abstractmethod
    def get_role_by_role(self, role) -> RoleTO:
        """Retrieve role by role"""
        
    @abstractmethod
    def get_user_role_in_analysis(self, user_id, analysis_id) -> RoleTO:
        """Retrieve the role of an user within an analysis"""

