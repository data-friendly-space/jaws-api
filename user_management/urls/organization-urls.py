"""User management URL Configuration"""
from django.urls import path

from user_management.interfaces.controllers.create_organization_controller import create_organization_controller

urlpatterns = [
    path('create', create_organization_controller, name='create-organization'),
]
