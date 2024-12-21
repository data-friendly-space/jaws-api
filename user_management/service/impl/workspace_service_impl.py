"""This module contains the workspace service implementation"""

from common.exceptions.exceptions import BadRequestException, NotFoundException
from common.helpers.query_options import QueryOptions
from common.use_case.get_all_uc import GetAllUC
from user_management.contract.io.create_workspace_in import CreateWorkspaceIn
from user_management.contract.io.invite_user_workspace_in import InviteUserWorkspaceIn
from user_management.repository.role_repository_impl import RoleRepositoryImpl
from user_management.repository.user_repository_impl import UserRepositoryImpl
from user_management.repository.workspace_repository_impl import WorkspaceRepositoryImpl
from user_management.service.workspace_service import WorkspaceService
from user_management.usecases.add_user_to_workspace_uc import AddUserToWorkspaceUC
from user_management.usecases.create_workspace_uc import CreateWorkspaceUC
from user_management.usecases.get_role_by_role_uc import GetRoleByRoleUC
from user_management.usecases.get_user_uc_by_filters_uc import GetUserByFiltersUC
from user_management.usecases.get_user_workspaces_by_filters_uc import GetUserWorkspacesByFiltersUC
from user_management.usecases.invite_user_to_workspace_uc import InviteUserToWorkspaceUC


class WorkspaceServiceImpl(WorkspaceService):
    """Workspace service implementation"""

    def __init__(self):
        self.get_all_workspaces_uc = GetAllUC.get_instance()
        self.create_workspace_uc = CreateWorkspaceUC.get_instance()
        self.get_user_by_filter_uc = GetUserByFiltersUC.get_instance()
        self.get_role_by_role_uc = GetRoleByRoleUC.get_instance()
        self.get_user_workspaces_by_filter_uc = GetUserWorkspacesByFiltersUC.get_instance()
        self.invite_user_to_workspace_uc = InviteUserToWorkspaceUC.get_instance()
        self.workspace_repository = WorkspaceRepositoryImpl()
        self.user_repository = UserRepositoryImpl()
        self.role_repository = RoleRepositoryImpl()
        self.add_user_to_workspace_uc = AddUserToWorkspaceUC.get_instance()

    def get_workspaces(self):
        """Retrieves the workspaces"""
        workspaces = self.get_all_workspaces_uc.exec(self.workspace_repository, None)
        if not workspaces:
            raise NotFoundException("Workspaces not found")
        return [workspace.to_dict() for workspace in workspaces]

    def create_workspace(self, create_workspace_in: CreateWorkspaceIn, creator_id: str):
        """Create a new workspace"""
        if not create_workspace_in.is_valid():
            raise BadRequestException("Workspace request is not valid: ", create_workspace_in.errors)
        data = create_workspace_in.validated_data
        facilitator = self.get_user_by_filter_uc.exec(self.user_repository, email=data['facilitator_email'])
        if not facilitator:
            raise NotFoundException("Facilitator not found")
        data['creator_id'] = creator_id
        data.pop('facilitator_email', None)
        data['facilitator_id'] = facilitator.id
        created_workspace = self.create_workspace_uc.exec(self.workspace_repository, data)
        role = self.get_role_by_role_uc.exec(self.role_repository, role="FACILITATOR")
        return self.add_user_to_workspace_uc.exec(self.workspace_repository, creator_id, created_workspace.id,
                                                  role.id).to_dict()

    def get_workspaces_by_user_id(self, user_id: str, query_options: QueryOptions):
        """Returns a list of workspaces with user role based on user id """
        workspaces = self.get_user_workspaces_by_filter_uc.exec(self.workspace_repository, query_options,
                                                                user_id=user_id)
        if not workspaces:
            raise NotFoundException("Workspaces not found")
        return [workspace.to_dict() for workspace in workspaces]
