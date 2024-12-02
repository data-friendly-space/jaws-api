class ServiceException(Exception):
    """Base exception for service layer"""
    pass


class BadRequestException(ServiceException):
    """Exception raised for invalid requests"""

    def __init__(self, message="Bad Request", errors=None):
        self.message = message
        self.errors = errors
        super().__init__(self.message)


class UnauthorizedException(ServiceException):
    """Exception raised for unauthorized access"""

    def __init__(self, message="Unauthorized", errors=None):
        self.message = message
        self.errors = errors
        super().__init__(self.message)


class ForbiddenException(ServiceException):
    """Exception raised for forbidden access"""

    def __init__(self, message="Forbidden", errors=None):
        self.message = message
        self.errors = errors
        super().__init__(self.message)


class NotFoundException(ServiceException):
    """Exception raised for not found resources"""

    def __init__(self, message="Not Found", errors=None):
        self.message = message
        self.errors = errors
        super().__init__(self.message)


class ConflictException(ServiceException):
    """Exception raised for conflict errors"""

    def __init__(self, message="Conflict", errors=None):
        self.message = message
        self.errors = errors
        super().__init__(self.message)


class InternalServerErrorException(ServiceException):
    """Exception raised for internal server errors"""

    def __init__(self, message="Internal Server Error", errors=None):
        self.message = message
        self.errors = errors
        super().__init__(self.message)
