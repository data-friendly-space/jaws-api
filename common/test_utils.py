"""Contains test utilities"""
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

from analysis.models.analysis import Analysis
from user_management.models.organization import Organization
from user_management.models.workspace import Workspace

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

def create_test_analysis(user):
    """Create all the structure fo an analysis"""
    organization = Organization.objects.create(name="TestOrganization2")
    workspace = Workspace.objects.create(
        title="TestWorksp2ace1",
        organization=organization,
        facilitator_id=user.id,
        creator_id=user.id,
    )
    test_analysis = Analysis.objects.create(
        title="TestAnalysis1",
        workspace_id=workspace.id,
        end_date="2024-12-17",
        creator_id=user.id,
    )

    return test_analysis
