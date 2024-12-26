"""This module contains the tests for the controllers"""

from django.test import TestCase
from django.urls import reverse

from analysis.models.analysis import Analysis
from common.test_utils import create_logged_in_client
from user_management.models.organization import Organization
from user_management.models.workspace import Workspace


class TestCreatePresignedUrlFileUploadController(TestCase):
    """TestCase for get presigned url for file upload"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.org = Organization.objects.create(name="TestOrganization2")
        self.workspace = Workspace.objects.create(
            title="TestWorkspace1",
            organization=self.org,
            facilitator_id=self.user.id,
            creator_id=self.user.id,
        )
        self.test_analysis = Analysis.objects.create(
            title="TestAnalysis1",
            workspace_id=self.workspace.id,
            end_date="2024-12-17",
            creator_id=self.user.id,
        )
        self.url = reverse("get_upload_file_url")

    def test_valid_data(self):
        """Test if creating a presigned url with valid data works"""
        valid_data = {"filename": "Prueba", "analysisId": 15}
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "url",
            response.data["payload"],
            "The payload must contain 'url' field"
        )
        self.assertIn(
            "fields",
            response.data["payload"],
            "The payload must contain 'fields' field",
        )
        self.assertIn(
            "AWSAccessKeyId",
            response.data["payload"]["fields"],
            "The 'fields' field must contain 'AWSAccessKeyId' field",
        )
        self.assertIn(
            "policy",
            response.data["payload"]["fields"],
            "The 'fields' field must contain 'policy' field"
        )
        self.assertIn(
            "signature",
            response.data["payload"]["fields"],
            "The 'fields' field must contain 'signature' field"
        )

    def test_invalid_data(self):
        """Test if creating a presigned url with invalid data fails"""
        invalid_data = {"filename": "Prueba", "asd": 15}
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 400)
