'''Module for handling the exceptions'''
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from common.exceptions.exceptions import (
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    ConflictException,
    InternalServerErrorException,
)
from common.helpers.api_responses import api_response_error


class ExceptionHandler(MiddlewareMixin):
    '''Handles the exceptions to avoid handling it within the app'''
    def process_exception(self, _request, exception):
        '''Process the exception and return a proper response'''
        if isinstance(exception, BadRequestException):
            response = api_response_error(
                exception.message, exception.errors, status.HTTP_400_BAD_REQUEST
            )
            return self.render_response(response)
        if isinstance(exception, UnauthorizedException):
            response = api_response_error(
                exception.message, exception.errors, status.HTTP_401_UNAUTHORIZED
            )
            return self.render_response(response)
        if isinstance(exception, ForbiddenException):
            response = api_response_error(
                exception.message, exception.errors, status.HTTP_403_FORBIDDEN
            )
            return self.render_response(response)
        if isinstance(exception, NotFoundException):
            response = api_response_error(
                exception.message, exception.errors, status.HTTP_404_NOT_FOUND
            )
            return self.render_response(response)
        if isinstance(exception, ConflictException):
            response = api_response_error(
                exception.message, exception.errors, status.HTTP_409_CONFLICT
            )
            return self.render_response(response)
        if isinstance(exception, InternalServerErrorException):
            response = api_response_error(
                exception.message,
                exception.errors,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            return self.render_response(response)
        # For any other exceptions, return a generic 500 error response
        response = api_response_error(
            "Internal Server Error",
            str(exception),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        return self.render_response(response)

    @staticmethod
    def render_response(response):
        '''Renders the response'''
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response
