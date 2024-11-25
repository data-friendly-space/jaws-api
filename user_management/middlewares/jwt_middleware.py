from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse

from user_management.interfaces.controllers.helpers.api_response import api_response


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = ['/jaws-api/user-management/users', '/jaws-api/user-management/sign-up',
                          '/jaws-api/user-management/sign-in', '/jaws-api/user-management/token-refresh',
                          '/jaws-api/user-management/session-verify', '/favicon.ico']
        if request.path not in excluded_paths:
            auth_header = request.headers.get('Authorization', None)
            if not auth_header or not auth_header.startswith('Bearer '):
                return api_response('Token not found', None, 401)

            token = auth_header.split(' ')[1]
            try:
                AccessToken(token)
            except Exception as e:
                return api_response('Invalid or expired Token', None, 401)
        return self.get_response(request)
