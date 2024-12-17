"""User management URL Configuration"""

from django.urls import path

from analysis.interfaces.controllers.get_analysis_controller import get_analysis_controller
from user_management.interfaces.controllers.create_workspace_controller import create_workspace_controller

urlpatterns = [
    path('create', create_workspace_controller, name='create_workspace'),
    #path('invite', invite_user_to_workspace_controller, name='invite_user_to_workspace'),
    path('<str:workspace_id>/analyses', get_analysis_controller, name='get_analysis_controller')
]
