from django.urls import path
from user_management.interfaces.controllers.create_user_controller import create_user_controller
from user_management.interfaces.controllers.get_users_controller import get_users_controller

urlpatterns = [
    path('users/', get_users_controller, name='users'),
    path("users/create", create_user_controller, name="create_user"),
]
