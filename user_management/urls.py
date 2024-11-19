from django.urls import path

from user_management.interfaces.controllers import get_users_controller
from user_management.interfaces.controllers.get_users_controller import get_users_controller

urlpatterns = [
    path('users/', get_users_controller, name='users'),
]
