"""This module contains the implementation of Workspace repository"""
from common.helpers.query_options import QueryOptions
from user_management.contract.repository.workspace_repository import WorkspaceRepository
from user_management.contract.to.user_workspace_role_to import UserWorkspaceRoleTO
from user_management.contract.to.user_workspace_to import UserWorkspaceTO
from user_management.contract.to.workspace_to import WorkspaceTO
from user_management.models import Workspace, UserWorkspaceRole


class WorkspaceRepositoryImpl(WorkspaceRepository):

    def get_user_workspaces_by_filters(self, **kwargs):
        filters = {key: value for key, value in kwargs.items() if value is not None}
        workspace_users = UserWorkspaceRole.objects.filter(**filters)
        return UserWorkspaceRoleTO.from_models(workspace_users)

    def get_workspace_users_by_workspace_id(self, workspace_id):
        workspace_users = UserWorkspaceRole.objects.filter(workspace_id=workspace_id)
        return UserWorkspaceTO.from_models(workspace_users)

    def delete_by_id(self, obj_id):
        """Delete workspace by id"""
        workspace = Workspace.objects.get(id=obj_id)
        return workspace.delete()

    def update(self, obj_id, data):
        """Update workspace by ID"""
        workspace = Workspace.objects.get(id=obj_id)
        for field, value in data.items():
            setattr(workspace, field, value)
        workspace.save()
        return workspace

    def get_by_id(self, obj_id):
        """Retrieve workspace by ID"""
        return Workspace.objects.filter(id=obj_id).first()

    def create(self, data):
        """Creates and retrieve new workspace"""
        workspace = Workspace.objects.create(**data)
        return WorkspaceTO.from_model(workspace)

    def get_all(self, query_options: QueryOptions):
        """Retrieves all workspaces"""
        return WorkspaceTO.from_models(Workspace.objects.all())

    def invite_user_to_workspace(self, data):
        """Invite user to workspace"""
        UserWorkspaceRole.objects.create(data)
