"""Contains the definition for the app"""
from django.apps import AppConfig


class FileManagementConfig(AppConfig):
    """app definition"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file_management'
