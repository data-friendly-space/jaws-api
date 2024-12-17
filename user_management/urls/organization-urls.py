"""User management URL Configuration"""
from django.urls import path

from user_management.interfaces.controllers.create_organization_controller import create_organization_controller
from user_management.interfaces.controllers.get_organization_users_controller import \
    get_organizations_users_by_user_id_controller
from user_management.interfaces.controllers.get_users_from_organization_by_role_controller import \
    get_users_from_organization_by_role_controller

urlpatterns = [
    path('create', create_organization_controller, name='create-organization'),
    #path('invite', invite_user_to_organization_controller, name='invite_organization_to_workspace'),
    path('users', get_organizations_users_by_user_id_controller, name='get-organizations-users-by-user-id'),
    path('<str:organization_id>/users/role/<str:role>', get_users_from_organization_by_role_controller,
         name='get_users_from_organization_by_role_controller'),
]
