"""This module contains the workspace service implementation"""
from abc import ABC, abstractmethod

from common.use_case.get_all_uc import GetAllUC
from user_management.service.workspace_service import WorkspaceService


class WorkspaceServiceImpl(WorkspaceService):
    """Workspace service implementation"""
    def __init__(self):
        self.get_all_workspaces_uc = GetAllUC.get_instance()
    @abstractmethod
    def get_workspaces(self):
        return WorkspaceSerial
        """Retrieves the workspaces"""

    @abstractmethod
    def create_workspace(self, template_name, workspace_name, facilitator_email, country):
        """Create a new workspace"""
