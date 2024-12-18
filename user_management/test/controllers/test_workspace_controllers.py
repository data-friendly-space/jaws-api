import uuid
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from analysis.models.analysis import Analysis
from common.test_utils import create_logged_in_client
from user_management.models import Organization, Role, Workspace


# Create your tests here.


class WorkspaceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.org = Organization.objects.create(name="TestOrganization5")
        self.workspace = Workspace.objects.create(title="TestWorkspace6", organization=self.org,
                                                  facilitator_id=self.user.id, creator_id=self.user.id)
        self.role = Role.objects.get_or_create(role="ADMIN")
        self.analysis = Analysis.objects.create(title="TestAnalysis1", workspace_id=self.workspace.id,
                                                end_date='2024-12-17', creator_id=self.user.id)

    def test_create_workspace(self):
        response = self.client.post(reverse('create_workspace'), {
            "title": "TestName1",
            "facilitator_email": "test@test.com",
            "organization_id": self.org.id,
        })

        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Workspace successfully created')

    def test_get_analysis_controller(self):
        response = self.client.get(reverse('get_analysis_controller', args=[str(self.workspace.id)]))

        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Analysis retrieved successfully.')
