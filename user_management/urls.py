from django.urls import path
from user_management.interfaces.controllers.create_user_controller import create_user_controller
from user_management.interfaces.controllers.get_users_controller import get_users_controller
from user_management.interfaces.controllers.refresh_token_controller import refresh_token_controller
from user_management.interfaces.controllers.sign_in_controller import sign_in_controller
from user_management.interfaces.controllers.sign_up_controller import sign_up_controller

urlpatterns = [
    path('users', get_users_controller, name='users'),
    path("users/create", create_user_controller, name="create_user"),
    path('sign-in', sign_in_controller, name='sign_in'),
    path('sign-up', sign_up_controller, name='sign_up'),

    path('token-refresh', refresh_token_controller, name='token_refresh'),
]
