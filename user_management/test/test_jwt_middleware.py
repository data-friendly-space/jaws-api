"""Contains the tests for the JWT middleware"""

import json
from unittest import mock
from unittest.mock import Mock, patch

from django.http import JsonResponse
from django.test import RequestFactory, TestCase
from rest_framework_simplejwt.tokens import AccessToken

from user_management.middlewares.jwt_middleware import JWTMiddleware
from user_management.models import User


class JWTMiddlewareTests(TestCase):
    """Contains the tests for the middleware"""

    def setUp(self):
        self.user = User.objects.create(email="testuser@gmail.com")

        self.get_response_mock = Mock(return_value=JsonResponse({"message": "Success"}))
        self.middleware = JWTMiddleware(self.get_response_mock)

        self.factory = RequestFactory()
        self.valid_token = str(AccessToken.for_user(self.user))

    def test_excluded_path(self):
        """Test that the middleware avoid public routes"""
        request = self.factory.get("/auth/login/google-oauth2/")
        response = self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Success"})

    def test_missing_authorization_header(self):
        """Test that returns 401 if the authentication header is not present"""
        request = self.factory.get("/protected/resource")
        response = self.middleware(request)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token_prefix(self):
        """Test that returns 401 if the prefix Bearer is not present"""
        request = self.factory.get(
            "/protected/resource", HTTP_AUTHORIZATION="Basic invalidtoken"
        )
        response = self.middleware(request)

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"detail": "Invalid token prefix."})

    @patch("user_management.models.User.objects.get")
    def test_valid_token(self, mock_get_user):
        """Test that a correct JWT is validated correctly"""
        mock_get_user.return_value = self.user
        request = self.factory.get(
            "/protected/resource", HTTP_AUTHORIZATION=f"Bearer {self.valid_token}"
        )
        middleware = JWTMiddleware(
            get_response=lambda request: JsonResponse({"message": "Success"})
        )

        response = middleware(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Success"})
        self.assertEqual(request.user, self.user)

    @mock.patch("rest_framework_simplejwt.tokens.AccessToken")
    def test_invalid_token(self, mock_access_token):
        """Test that a invalid jwt returns 401"""
        mock_access_token.return_value = {"user_id": self.user.id}

        request = self.factory.get(
            "/protected/resource", HTTP_AUTHORIZATION="Bearer invalidtoken"
        )
        response = self.middleware(request)

        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response_data["detail"], "Invalid token.")
