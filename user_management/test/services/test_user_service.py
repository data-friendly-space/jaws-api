"""Contains the tests for the user service"""
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from common.exceptions.exceptions import BadRequestException, UnauthorizedException
from common.test_utils import create_logged_in_client, User
from user_management.contract.io.sign_in_in import SignInIn
from user_management.contract.io.sign_up_in import SignUpIn
from user_management.contract.to.user_to import UserTO
from user_management.interfaces.serializers.token_serializer import UserTokenSerializer
from user_management.service.impl.users_service_impl import UsersServiceImpl


class TestUserService(TestCase):
    """Contains the tests for the user service"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = UsersServiceImpl()
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)
        self.invalid_refresh_token = "invalid.token.here"

    def test_sign_up(self):
        sign_in_up = SignUpIn(
            data={"name": "test1", "lastname": "testlast323", "email": "testuser24@gmail.com", "password": "password"})
        self.service.sign_up(sign_in_up)
        user = User.objects.get(email="testuser24@gmail.com")
        self.assertEqual(user.name, "test1")
        self.assertEqual(user.lastname, "testlast323")
        self.assertTrue(user.check_password("password"))

    def test_sign_up_missing_field(self):
        sign_in_up = SignUpIn(
            data={"name": "test1", "lastname": "testlast323", "email": "", "password": ""})
        with self.assertRaises(BadRequestException) as context:
            self.service.sign_up(sign_in_up)
        self.assertEqual(str(context.exception), "All fields are mandatory")

    def test_sign_up_user_already_exists(self):
        sign_in_up = SignUpIn(
            data={"name": "test1", "lastname": "testlast323", "email": "testuser24@gmail.com", "password": "password"})
        self.service.sign_up(sign_in_up)
        with self.assertRaises(BadRequestException) as context:
            self.service.sign_up(sign_in_up)
        self.assertEqual(str(context.exception), "User already exists")

    def test_sign_in(self):
        sign_in_in = SignInIn(
            data={"email": "testuser24@gmail.com", "password": "password"})
        sign_in_up = SignUpIn(
            data={"name": "test1", "lastname": "testlast323", "email": "testuser24@gmail.com", "password": "password"})
        self.service.sign_up(sign_in_up)
        response = self.service.sign_in(sign_in_in)
        self.assertEqual(response.get('user')['name'], "test1")
        self.assertEqual(response.get('user')['lastname'], "testlast323")

    def test_sign_in_incorrect_password_email(self):
        sign_in_up = SignUpIn(
            data={"name": "test1", "lastname": "testlast323", "email": "testuser24@gmail.com", "password": "password"})
        sign_in_in = SignInIn(
            data={"email": "testuser24@gmail.com", "password": "passwo2rd"})
        self.service.sign_up(sign_in_up)
        with self.assertRaises(BadRequestException) as context:
            self.service.sign_in(sign_in_in)
        self.assertEqual(str(context.exception), "Incorrect email or password")

    def test_refresh_token_valid(self):
        response = self.service.refresh_token(self.refresh_token)
        self.assertIsNotNone(response)

    def test_refresh_token_invalid(self):
        sign_in_up = SignUpIn(
            data={"name": "test1", "lastname": "testlast323", "email": "testuser24@gmail.com", "password": "password"})
        sign_in_in = SignInIn(
            data={"email": "testuser24@gmail.com", "password": "password"})
        self.service.sign_up(sign_in_up)
        self.service.sign_in(sign_in_in)
        with self.assertRaises(Exception) as context:
            self.service.refresh_token(self.refresh_token + "wdasdasd")
        self.assertEqual(str(context.exception), 'Token is invalid or expired')

    def test_refresh_token_missing(self):
        with self.assertRaises(BadRequestException) as context:
            self.service.refresh_token("")
        self.assertEqual(str(context.exception), "Refresh token is required.")

class TestSignInWithAccessToken(TestCase):
    """Test the method for signing in with an access token"""

    def setUp(self):
        self.service = UsersServiceImpl()

    def test_token_not_provided(self):
        """Test that calling the method with no token raises an exception"""
        with self.assertRaises(UnauthorizedException):
            self.service.sign_in_with_access_token(None)

    def test_token_not_valid(self):
        """Test that using an unvalid token raises an UnauthorizedException"""
        token = "invalid-token"
        with self.assertRaises(UnauthorizedException):
            self.service.sign_in_with_access_token(token)

    def test_user_not_found(self):
        """Test that using a false JWT raises a BadRequestException"""
        token_user_not_existing = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwMzQyNDQ2LCJpYXQiOjE3MzQzNDI0NDYsImp0aSI6IjhjZGJiOTUxYzc4NTQ2MmRhNTc3NmRhM2FlNDUwYjBhIiwidXNlcl9pZCI6IjgxYjA0ODQ4LTZjMGQtNDU1Mi04MzBiLTJiNmEzMjcyMTdlNiJ9.OBgYSunsdmIAjI6IR_xsOoUcaRQRvZxuCvPC0kkbW1Q"
        with self.assertRaises(BadRequestException):
            self.service.sign_in_with_access_token(token_user_not_existing)

    def test_user_existing(self):
        """Test that using a valid token returns a valid response"""
        user = User.objects.create(
            name="TestName",
            lastname="TestLastname",
            email="test@test.com",
            password="testpassword",
        )
        user_to = UserTO.from_model(user)
        valid_token = AccessToken.for_user(user)
        response = self.service.sign_in_with_access_token(str(valid_token))
        response_expected = UserTokenSerializer(user_to).data
        self.assertEqual(response["user"]["id"], response_expected["user"]["id"])
