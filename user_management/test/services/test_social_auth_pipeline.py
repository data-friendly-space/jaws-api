"""Test the pipeline of social auth"""
from unittest.mock import Mock, patch
from urllib.parse import parse_qs, urlparse

from django.http import HttpResponseRedirect
from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken

from common.exceptions.exceptions import UnauthorizedException

from ...social_auth.pipeline import redirect_to_next_with_token


class TestSocialAuthPipeline(TestCase):
    """Test the social auth pipeline"""
    def setUp(self):
        self.mock_backend = Mock()
        self.mock_backend.strategy.session_get = Mock()

        self.mock_user = Mock()
        self.mock_response = {"access_token": "mock_access_token"}

    def test_redirect_with_valid_next_and_access_token(self):
        """Test redirect with valid next url and valid access token"""
        next_url = "http://someurl.com/dashboard"
        self.mock_backend.strategy.session_get.return_value = next_url

        with patch.object(AccessToken, "for_user", return_value="mock_jwt_token"):
            # Llamar a la función
            response = redirect_to_next_with_token(
                backend=self.mock_backend,
                user=self.mock_user,
                response=self.mock_response,
            )

            # Verificar que la respuesta es un redireccionamiento
            self.assertIsInstance(response, HttpResponseRedirect)

            # Verificar la URL de redirección
            parsed_url = urlparse(response.url)
            self.assertEqual(parsed_url.scheme, "http")
            self.assertEqual(parsed_url.netloc, "someurl.com")
            self.assertEqual(parsed_url.path, "/dashboard")

            # Verificar que el token JWT está en los parámetros de consulta
            query_params = parse_qs(parsed_url.query)
            self.assertIn("access", query_params)
            self.assertEqual(query_params["access"], ["mock_jwt_token"])

    def test_raises_exception_when_no_access_token(self):
        """Test that if no access token was provided the pipeline fails"""
        self.mock_response.pop("access_token")

        with self.assertRaises(UnauthorizedException):
            redirect_to_next_with_token(
                backend=self.mock_backend,
                user=self.mock_user,
                response=self.mock_response,
            )

    def test_raises_exception_when_no_next_url(self):
        """Test that if no next url was provided, the pipeline fails"""
        self.mock_backend.strategy.session_get.return_value = None

        with self.assertRaises(UnauthorizedException):
            redirect_to_next_with_token(
                backend=self.mock_backend,
                user=self.mock_user,
                response=self.mock_response,
            )
