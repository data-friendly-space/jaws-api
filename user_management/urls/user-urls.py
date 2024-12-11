"""User management URL Configuration"""
from django.urls import path

from user_management.interfaces.controllers.create_workspace_controller import create_workspace_controller
from user_management.interfaces.controllers.get_roles_controller import get_roles_controller
from user_management.interfaces.controllers.get_users_controller import get_users_controller
from user_management.interfaces.controllers.refresh_token_controller import refresh_token_controller
from user_management.interfaces.controllers.sign_in_controller import sign_in_controller
from user_management.interfaces.controllers.sign_up_controller import sign_up_controller
from user_management.interfaces.controllers.verify_token_controller import verify_token_controller

urlpatterns = [
    path('users', get_users_controller, name='get_users'),
    path('roles/', get_roles_controller, name='get_roles'),
    path('roles/<slug:space>/', get_roles_controller, name='get_roles_by_space'),
    #path("users/create", create_user_controller, name="create_user"),
    path('sign-in', sign_in_controller, name='sign_in'),
    path('sign-up', sign_up_controller, name='sign_up'),

    path('token-refresh', refresh_token_controller, name='token_refresh'),

    path('session-verify', verify_token_controller, name='session_verify'),

    path('workspaces/create', create_workspace_controller, name='create_workspace_controller'),
]
