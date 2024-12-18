"""Contains the middleware for user authentication"""
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from user_management.models import User


class JWTMiddleware:
    """Authenticate the user"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = [
            '/auth/complete/google-oauth2/',
            '/auth/login/google-oauth2/',
            '/jaws-api/user-management/sign-in-with-access-token',
            '/jaws-api/csrf', 
            '/jaws-api/user-management/sign-up',
            '/jaws-api/user-management/users',
            '/jaws-api/user-management/sign-in', 
            '/jaws-api/user-management/token-refresh',
            '/jaws-api/user-management/session-verify', 
            '/favicon.ico']


        if request.path in excluded_paths:
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return JsonResponse({'detail': 'Authorization header missing.'}, status=401)

        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                return JsonResponse({'detail': 'Invalid token prefix.'}, status=401)

            decoded_token = AccessToken(token)
            request.user = User.objects.get(id=decoded_token['user_id'])

        except (TokenError, InvalidToken) as e:
            return JsonResponse({'detail': 'Invalid token.', 'error': str(e)}, status=401)
        return self.get_response(request)