from django.apps import AppConfig
from health_check.plugins import plugin_dir

from health_checks.postgresql_health_check import PostgreSQLHealthCheck


class HealthChecksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'health_checks'

    def ready(self):
        plugin_dir.register(PostgreSQLHealthCheck)
