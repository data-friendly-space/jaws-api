"""This module contains the implementation of Workspace repository"""
from common.helpers.query_options import QueryOptions
from user_management.contract.repository.workspace_repository import WorkspaceRepository
from user_management.models import Workspace


class WorkspaceRepositoryImpl(WorkspaceRepository):
    def get_workspace_users(self, workspace_id):
        """Get workspace users by workspace id"""
        pass

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
        return Workspace.objects.create(data)

    def get_all(self, query_options: QueryOptions):
        """Retrieves all workspaces"""
        return Workspace.objects.all()
