from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions.exceptions import BadRequestException
from common.test_utils import create_logged_in_client
from user_management.service.impl.users_service_impl import UsersServiceImpl


class TestAnalysisService(TestCase):

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = UsersServiceImpl()
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)
        self.invalid_refresh_token = "invalid.token.here"

    def test_sign_up(self):
        response = self.service.sign_up("test1", "testlast323", "testuser24@gmail.com", "password")
        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User successfully created')

    def test_sign_up_missing_field(self):
        with self.assertRaises(BadRequestException) as context:
            self.service.sign_up("test1", "testlast323", "testuser24@gmail.com", "")
        self.assertEqual(str(context.exception), "All fields are mandatory")

    def test_sign_up_user_already_exists(self):
        self.service.sign_up("test1", "testlast323", "testuser24@gmail.com", "password")
        with self.assertRaises(BadRequestException) as context:
            self.service.sign_up("test1 ", "testlast323", "testuser24@gmail.com", "password")
        self.assertEqual(str(context.exception), "User already exists")

    def test_sign_in(self):
        self.service.sign_up("test1", "testlast323", "testuser24@gmail.com", "password")
        response = self.service.sign_in("testuser24@gmail.com", "password")
        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User authenticated')

    def test_sign_in_incorrect_password_email(self):
        self.service.sign_up("test1", "testlast323", "testuser24@gmail.com", "password2")
        with self.assertRaises(BadRequestException) as context:
            self.service.sign_in("testuser24@gmail.com", "password")
        self.assertEqual(str(context.exception), "Incorrect email or password")

    def test_refresh_token_valid(self):
        response = self.service.refresh_token(self.refresh_token)
        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Access granted")
        self.assertIn("jwt_access_token", response.data['payload'])

    def test_refresh_token_invalid(self):
        self.service.sign_up("test1", "testlast323", "testuser24@gmail.com", "password2")
        self.service.sign_in("testuser24@gmail.com", "password2")
        with self.assertRaises(Exception) as context:
            self.service.refresh_token(self.refresh_token + "wdasdasd")
        self.assertEqual(str(context.exception), 'Token is invalid or expired')

    def test_refresh_token_missing(self):
        with self.assertRaises(BadRequestException) as context:
            self.service.refresh_token("")
        self.assertEqual(str(context.exception), "Refresh token is required.")
