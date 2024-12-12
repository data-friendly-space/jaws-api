"""This module contains the workspace service implementation"""

from common.exceptions.exceptions import BadRequestException, NotFoundException
from common.use_case.get_all_uc import GetAllUC
from user_management.contract.io.create_workspace_in import CreateWorkspaceIn
from user_management.contract.io.invite_user_workspace_in import InviteUserWorkspaceIn
from user_management.repository.workspace_repository_impl import WorkspaceRepositoryImpl
from user_management.service.workspace_service import WorkspaceService
from user_management.usecases.create_workspace_uc import CreateWorkspaceUC
from user_management.usecases.get_user_uc_by_filters_uc import GetUserByFiltersUC
from user_management.usecases.get_user_workspaces_by_filters_uc import GetUserWorkspacesByFiltersUC
from user_management.usecases.get_workspace_users_by_workspace_id_uc import GetWorkspaceUsersByWorkspaceIdUC
from user_management.usecases.invite_user_to_workspace_uc import InviteUserToWorkspaceUC


class WorkspaceServiceImpl(WorkspaceService):
    """Workspace service implementation"""

    def __init__(self):
        self.get_all_workspaces_uc = GetAllUC.get_instance()
        self.create_workspace_uc = CreateWorkspaceUC.get_instance()
        self.get_user_by_filter_uc = GetUserByFiltersUC.get_instance()
        self.get_user_workspaces_by_filter_uc = GetUserWorkspacesByFiltersUC.get_instance()
        self.get_workspaces_users_by_workspace_id = GetWorkspaceUsersByWorkspaceIdUC.get_instance()
        self.invite_user_to_workspace_uc = InviteUserToWorkspaceUC.get_instance()
        self.workspace_repository = self.workspace_repository
    def get_workspaces(self):
        """Retrieves the workspaces"""
        workspaces = self.get_all_workspaces_uc.exec(self.workspace_repository)
        if not workspaces:
            raise NotFoundException("Workspaces not found")
        return [workspace.to_dict() for workspace in workspaces]

    def create_workspace(self, create_workspace_in: CreateWorkspaceIn, creator_id: str):
        """Create a new workspace"""
        if not create_workspace_in.is_valid():
            raise BadRequestException("Workspace request is not valid: ", create_workspace_in.errors)
        data = create_workspace_in.validated_data
        data['creator_id'] = creator_id
        return self.create_workspace_uc.exec(self.workspace_repository, data).to_dict()

    def get_workspaces_by_user_id(self, user_id: str):
        """Returns a list of workspaces with user role based on user id """
        workspaces = self.get_user_workspaces_by_filter_uc.exec(self.workspace_repository, user_id=user_id)
        if not workspaces:
            raise NotFoundException("Workspaces not found")
        return [workspace.to_dict() for workspace in workspaces]

    def get_workspace_users_by_workspace_id(self, workspace_id: str):
        """Returns a list of workspaces based on workspace id """
        workspaces = self.get_workspaces_users_by_workspace_id.exec(self.workspace_repository,
                                                                    workspace_id=workspace_id)
        if not workspaces:
            raise NotFoundException("Workspaces not found")
        return [workspace.to_dict() for workspace in workspaces]

    def invite_user_to_workspace(self, invite_user_in: InviteUserWorkspaceIn):
        if not invite_user_in.is_valid():
            raise BadRequestException("Invite user request is not valid: ", invite_user_in.errors)
        data = invite_user_in.validated_data
        self.invite_user_to_workspace_uc.exec(self.workspace_repository,data)
