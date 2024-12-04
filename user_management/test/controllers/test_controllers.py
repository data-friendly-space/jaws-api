from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from common.test_utils import create_logged_in_client


# Create your tests here.


class UserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.mockUser = {
            "name": "TestName1",
            "lastname": "TestLastname1",
            "email": "test1@test.com",
            "password": "testpassword1"
        }

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.url_session_verify = reverse("session_verify")

        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)

        self.url_refresh = reverse("token_refresh")

    def test_get_users(self):
        response = self.client.get(reverse("get_users"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_up(self):
        response = self.client.post(reverse("sign_up"), self.mockUser)
        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User successfully created')

    def test_sign_up_missing_field(self):
        # Bad request Exception caused by missing value
        self.mockUser['password'] = ''
        response = self.client.post(reverse("sign_up"), self.mockUser)
        self.assertEqual(response.data['status'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'All fields are mandatory')

    def test_sign_up_user_already_exists(self):
        # Bad request Exception caused by User already exists
        self.client.post(reverse("sign_up"), self.mockUser)
        mocked_user = MagicMock()
        mocked_user.email = "test@example.com"

        response = self.client.post(reverse("sign_up"), self.mockUser)
        self.assertEqual(response.data['status'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "User already exists")

    def test_sign_in(self):
        self.client.post(reverse("sign_up"), self.mockUser)
        response = self.client.post(reverse("sign_in"),
                                    {'email': self.mockUser['email'], 'password': self.mockUser['password']})
        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "User authenticated")

    def test_sign_in_bad_credentials(self):
        response = self.client.post(reverse("sign_in"), {'email': self.user.email, 'password': 'testpass'})
        self.assertEqual(response.data['status'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Incorrect email or password')

    def test_session_verify_valid_token(self):
        response = self.client.get(
            self.url_session_verify,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Is authenticated")
        self.assertTrue(response.data['payload']['isAuthenticated'])

    def test_session_verify_invalid_token(self):
        response = self.client.get(
            self.url_session_verify,
            HTTP_AUTHORIZATION="Bearer invalid.token.here"
        )

        self.assertEqual(response.data['status'], status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], "Session expired")
        self.assertFalse(response.data['errors']['is_authenticated'])

    def test_refresh_token_valid(self):
        response = self.client.post(
            self.url_refresh,
            {"refresh": self.refresh_token},
            format="json"
        )

        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Access granted")
        self.assertIn("jwt_access_token", response.data['payload'])

    def test_refresh_token_invalid(self):
        response = self.client.post(
            self.url_refresh,
            {"refresh": "invalid.token.here"},
            format="json"
        )

        self.assertEqual(response.data['status'], status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['errors'], 'Token is invalid or expired')

    def test_refresh_token_missing(self):
        response = self.client.post(
            self.url_refresh,
            {"refresh": ""},
            format="json"
        )

        self.assertEqual(response.data['status'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Refresh token is required.")
