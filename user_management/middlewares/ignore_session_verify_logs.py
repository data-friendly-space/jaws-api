import logging


class IgnoreSessionVerifyLogFilter(logging.Filter):
    def filter(self, record):
        return '/jaws-api/user-management/session-verify' not in record.getMessage()
