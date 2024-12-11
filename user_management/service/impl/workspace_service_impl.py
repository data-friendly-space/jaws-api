"""This module contains the workspace service implementation"""

from common.exceptions.exceptions import BadRequestException
from common.use_case.get_all_uc import GetAllUC
from user_management.contract.io.create_workspace_in import CreateWorkspaceIn
from user_management.repository.workspace_repository_impl import WorkspaceRepositoryImpl
from user_management.service.workspace_service import WorkspaceService
from user_management.usecases.create_workspace_uc import CreateWorkspaceUC
from user_management.usecases.get_user_uc_by_filters import GetUserByFiltersUC
from user_management.usecases.get_user_workspaces_by_filters import GetUserWorkspacesByFiltersUC
from user_management.usecases.get_workspace_users_by_workspace_id import GetWorkspaceUsersByWorkspaceIdUC


class WorkspaceServiceImpl(WorkspaceService):
    """Workspace service implementation"""

    def __init__(self):
        self.get_all_workspaces_uc = GetAllUC.get_instance()
        self.create_workspace_uc = CreateWorkspaceUC.get_instance()
        self.get_user_by_filter_uc = GetUserByFiltersUC.get_instance()
        self.get_user_workspaces_by_filter_uc = GetUserWorkspacesByFiltersUC.get_instance()
        self.get_workspaces_users_by_workspace_id = GetWorkspaceUsersByWorkspaceIdUC.get_instance()

    def get_workspaces(self):
        """Retrieves the workspaces"""
        workspaces = self.get_all_workspaces_uc.exec(WorkspaceRepositoryImpl())
        return [workspace.to_dict() for workspace in workspaces]

    def create_workspace(self, create_workspace_in: CreateWorkspaceIn):
        """Create a new workspace"""
        if not create_workspace_in.is_valid():
            raise BadRequestException("Workspace request is not valid: ", create_workspace_in.errors)
        data = create_workspace_in.validated_data

        return self.create_workspace_uc.exec(WorkspaceRepositoryImpl(), data).to_dict()

    def get_workspaces_by_user_id(self, user_id: str):
        """Returns a list of workspaces with user role based on user id """
        workspaces = self.get_user_workspaces_by_filter_uc.exec(WorkspaceRepositoryImpl(), user_id=user_id)
        return [workspace.to_dict() for workspace in workspaces]

    def get_workspace_users_by_workspace_id(self, workspace_id: str):
        """Returns a list of workspaces based on workspace id """
        workspaces = self.get_workspaces_users_by_workspace_id.exec(WorkspaceRepositoryImpl(),
                                                                    workspace_id=workspace_id)
        return [workspace.to_dict() for workspace in workspaces]
