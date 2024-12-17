
from unittest.mock import patch, MagicMock

from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions.exceptions import BadRequestException
from common.test_utils import create_logged_in_client, User
from user_management.service.impl.users_service_impl import UsersServiceImpl


class TestUserService(TestCase):

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = UsersServiceImpl()
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)
        self.invalid_refresh_token = "invalid.token.here"

    def test_sign_up(self):
        self.service.sign_up("test1", "testlast323", "testuser24@gmail.com", "password")
        user = User.objects.get(email="testuser24@gmail.com")
        self.assertEqual(user.name, "test1")
        self.assertEqual(user.lastname, "testlast323")
        self.assertTrue(user.check_password("password"))

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
        self.assertEqual(response.get('user')['name'], "test1")
        self.assertEqual(response.get('user')['lastname'], "testlast323")

    def test_sign_in_incorrect_password_email(self):
        self.service.sign_up("test1", "testlast323", "testuser24@gmail.com", "password2")
        with self.assertRaises(BadRequestException) as context:
            self.service.sign_in("testuser24@gmail.com", "password")
        self.assertEqual(str(context.exception), "Incorrect email or password")

    def test_refresh_token_valid(self):
        response = self.service.refresh_token(self.refresh_token)
        self.assertIsNotNone(response)

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
