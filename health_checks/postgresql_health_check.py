from django.db import connection
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException


class PostgreSQLHealthCheck(BaseHealthCheckBackend):
    def check_status(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception as e:
            self.add_error(HealthCheckException(f"PostgreSQL Health Check failed: {str(e)}"))

    def identifier(self):
        return self.__class__.__name__
