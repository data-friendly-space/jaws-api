import uuid
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from analysis.models.analysis import Analysis
from common.test_utils import create_logged_in_client
from user_management.models import Organization, Role, Workspace, UserWorkspaceRole


# Create your tests here.


class WorkspaceTestCase(TestCase):

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
        self.org = Organization.objects.create(name="TestOrganization1")
        self.workspace = Workspace.objects.create(title="TestWorkspace1", organization=self.org,
                                                  facilitator_id=self.user.id, creator_id=self.user.id)
        self.role = Role.objects.get_or_create(role="ADMIN")
        self.analysis = Analysis.objects.create(title="TestAnalysis1", workspace_id=self.workspace.id,
                                                end_date='2024-12-17', creator_id=self.user.id)
        UserWorkspaceRole.objects.create(user_id=self.user.id, role_id=self.role[0].id, workspace_id=self.workspace.id)

    def test_get_users(self):
        response = self.client.get(reverse('get_users'))

        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Users retrieved successfully')

    def test_user_workspaces(self):
        response = self.client.get(reverse('get_user_logged_workspaces_controller'))

        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Workspaces retrieved successfully')

    def test_user_organizations(self):
        response = self.client.get(reverse('get_available_organizations_by_user_id'))

        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Organizations retrieved successfully')
