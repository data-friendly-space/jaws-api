'''This module contains the permission repository'''
from abc import ABC, abstractmethod

from common.repository.base_repository import BaseRepository
from user_management.contract.to.permission_to import PermissionTO


class PermissionRepository(BaseRepository, ABC):
    '''Permission repository'''
