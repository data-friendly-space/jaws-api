"""User management URL Configuration"""
from django.urls import path

from user_management.interfaces.controllers.create_workspace_controller import create_workspace_controller
from user_management.interfaces.controllers.get_workspace_by_user_id_controller import \
    get_workspace_by_user_id_controller
from user_management.interfaces.controllers.get_workspace_users_controller import get_workspace_users_controller
from user_management.interfaces.controllers.invite_user_to_workspace_controller import \
    invite_user_to_workspace_controller

urlpatterns = [
    path('create', create_workspace_controller, name='create_workspace'),
    path('invite', invite_user_to_workspace_controller, name='invite_user_to_workspace'),
    path('<str:workspace_id>/users', get_workspace_users_controller, name='get-workspaces-users-by-workspace-id'),
    path('user/<slug:user_id>', get_workspace_by_user_id_controller, name='get-workspaces-by-user-id'),
]
