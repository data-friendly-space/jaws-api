"""Contains test utilities"""
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_logged_in_client():
    """Create a user and log him in"""
    user = User.objects.create(
        name="TestName",
        lastname="TestLastname",
        email="test@test.com",
        password="testpassword",
    )
    refresh = RefreshToken.for_user(user)
    client = Client()
    client.force_login(user)
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {str(refresh.access_token)}"
    return client, user
