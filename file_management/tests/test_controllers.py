"""This module contains the tests for the controllers"""

from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.urls import reverse

from analysis.models.analysis import Analysis
from common.exceptions.exceptions import BadRequestException
from common.test_utils import create_logged_in_client
from file_management.models.dataset import Dataset
from user_management.models.organization import Organization
from user_management.models.role import Role
from user_management.models.user_analysis_role import UserAnalysisRole
from user_management.models.workspace import Workspace


class TestCreatePresignedUrlFileUploadController(TestCase):
    """TestCase for get presigned url for file upload"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.url = reverse("get_upload_file_url")

    @patch(
        "file_management.interfaces.controllers.create_presigned_url_upload_file_controller.FileManagementServiceImpl"
    )
    def test_valid_data(self, mock_service):
        """Test if creating a presigned url with valid data works"""
        mock_service_instance = MagicMock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.create_presigned_url_upload_file.return_value = {
            "url": "https://example.com/upload"
        }
        valid_data = {"filename": "test.csv", "analysisId": 1}
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["payload"], {"url": "https://example.com/upload"}
        )
        mock_service_instance.create_presigned_url_upload_file.assert_called_once_with(
            self.user, "test.csv", 1
        )

    def test_missing_fields(self):
        """Test that calling the api with missing fields fails"""
        invalid_data = {"filename": "test.csv"}

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("All fields are required", response.data["message"])

    @patch(
        "file_management.interfaces.controllers.create_presigned_url_upload_file_controller.FileManagementServiceImpl"
    )
    def test_invalid_data(self, mock_service):
        """Test if creating a presigned url with invalid data fails"""
        mock_service_instance = MagicMock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.create_presigned_url_upload_file.side_effect = Exception()

        valid_data = {"filename": "test.csv", "analysisId": 1, "sizeBytes": 12345}

        response = self.client.post(self.url, valid_data)

        self.assertEqual(response.status_code, 500)

class TestCreatePresignedUrlDownloadFileController(TestCase):
    """Contains the test cases for the enpodint to getting url for downloading a dataset"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.url = reverse("get_download_file_url")

    @patch(
        "file_management.interfaces.controllers.create_presigned_url_download_file_controller.FileManagementServiceImpl"
    )
    def test_empty_dataset(self, mock_service):
        """Test that if the dataset is invalid or empty it raises an exception"""
        mock_service_instance = MagicMock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.create_presigned_url_download_file.side_effect = BadRequestException()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 400)

    @patch(
        "file_management.interfaces.controllers.create_presigned_url_download_file_controller.FileManagementServiceImpl"
    )
    def test_valid_dataset(self, mock_service):
        """Test that if the dataset is present and valid it works"""
        mock_service_instance = MagicMock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.create_presigned_url_download_file.return_value = [
            {
                "id": "cd516de1-354c-46b0-873b-11d2f9871287",
                "uploadedBy": "910c285d-d9a9-4d2c-af4e-31f4fb93a1c4",
                "sizeBytes": 10485760,
                "createdAt": "2024-12-30T17:06:40.705037Z",
                "updatedAt": "2024-12-30T17:06:40.710246Z",
                "mimeType": "text/csv",
                "url": "https://testUrl",
                "filename": "Prueba3.txt"
            },
            {
                "id": "de98223f-cb5d-4512-88a5-c143c55a2775",
                "uploadedBy": "910c285d-d9a9-4d2c-af4e-31f4fb93a1c4",
                "sizeBytes": 10485760,
                "createdAt": "2024-12-30T17:20:48.556865Z",
                "updatedAt": "2024-12-30T17:20:48.561312Z",
                "mimeType": "text/csv",
                "url": "https://testUrl",
                "filename": "Prueba3.txt"
            }
        ]
        dataset_id = 12345
        response = self.client.post(self.url + f"?dataset_id={dataset_id}")

        self.assertEqual(response.status_code, 200)
        mock_service_instance.create_presigned_url_download_file.assert_called_once()

class TestGetDatasetsFromAnalysis(TestCase):
    """Contains the test cases for getting the datasets from an analysis id"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.url = reverse("get_analysis_datasets")
        self.org = Organization.objects.create(name="TestOrganization2")
        self.workspace = Workspace.objects.create(
            title="TestWorksp2ace1",
            organization=self.org,
            facilitator_id=self.user.id,
            creator_id=self.user.id,
        )
        self.analysis = Analysis.objects.create(
            title="TestAnalysis1",
            workspace_id=self.workspace.id,
            end_date="2024-12-17",
            creator_id=self.user.id,
        )
        self.analysis.datasets.add(
            Dataset.objects.create(
                filename="test.csv",
                url="http://testurl/test.csv",
                uploaded_by=self.user,
                size_bytes=12345
            )
        )
        UserAnalysisRole.objects.create(
            user=self.user,
            analysis=self.analysis,
            role=Role.objects.first()
        )

    def test_call_without_analysis_id_fails(self):
        """Tests that if the query param analysis_id is not present it raises an exception"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_call_with_valid_data_works(self):
        """Test that if the analysis_id is present and valid works"""
        response = self.client.get(self.url + f"?analysis_id={self.analysis.id}")

        self.assertEqual(response.status_code, 200)
