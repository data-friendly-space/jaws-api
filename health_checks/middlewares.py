import logging


class IgnoreHealthCheckLogFilter(logging.Filter):
    def filter(self, record):
        # Ignore logs containing the specific health check path
        return '/jaws-api/health' not in record.getMessage()
