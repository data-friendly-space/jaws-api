"""This module contains the tests for the controllers"""

from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.urls import reverse

from common.test_utils import create_logged_in_client


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

        valid_data = {"filename": "test.csv", "analysisId": 1}

        response = self.client.post(self.url, valid_data)

        self.assertEqual(response.status_code, 500)
