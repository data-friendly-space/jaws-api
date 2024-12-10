"""This module contains the workspace service implementation"""

from common.exceptions.exceptions import BadRequestException
from common.use_case.get_all_uc import GetAllUC
from user_management.contract.io.create_workspace_in import CreateWorkspaceIn
from user_management.interfaces.serializers.workspace_serializer import WorkspaceSerializer
from user_management.repository.workspace_repository_impl import WorkspaceRepositoryImpl
from user_management.service.workspace_service import WorkspaceService
from user_management.usecases.create_workspace_uc import CreateWorkspaceUC


class WorkspaceServiceImpl(WorkspaceService):
    """Workspace service implementation"""

    def __init__(self):
        self.get_all_workspaces_uc = GetAllUC.get_instance()
        self.create_workspace_uc = CreateWorkspaceUC.get_instance()

    def get_workspaces(self):
        """Retrieves the workspaces"""
        return WorkspaceSerializer(self.get_all_workspaces_uc.exec(WorkspaceRepositoryImpl()), many=True).data

    def create_workspace(self, request: CreateWorkspaceIn):
        """Create a new workspace"""
        if not request.is_valid():
            raise BadRequestException("Workspace request is not valid: ", request.errors)
        data = request.validated_data
        return WorkspaceSerializer(self.create_workspace_uc.exec(WorkspaceRepositoryImpl(), data)).data

    def get_workspace_users(self, workspace_id):
        pass

