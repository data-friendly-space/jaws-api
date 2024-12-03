'''Module for the configuration of analysis app'''
from django.apps import AppConfig


class AnalysisConfig(AppConfig):
    '''Analysis configurations'''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analysis'
