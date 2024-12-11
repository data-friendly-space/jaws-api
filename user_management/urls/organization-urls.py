"""User management URL Configuration"""
from django.urls import path

from user_management.interfaces.controllers.create_organization_controller import create_organization_controller
from user_management.interfaces.controllers.get_organization_by_user_id_controller import \
    get_organization_by_user_id_controller
from user_management.interfaces.controllers.get_organization_users_controller import get_organization_users_controller

urlpatterns = [
    path('create', create_organization_controller, name='create-organization'),
    path('<str:organization_id>/users', get_organization_users_controller,
         name='get-organizations-users-by-organization-id'),
    path('user/<slug:user_id>', get_organization_by_user_id_controller, name='get-organizations-by-user-id'),
]
