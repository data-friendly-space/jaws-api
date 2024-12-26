"""This module contains the tests for the services"""

from unittest.mock import MagicMock
from django.test import SimpleTestCase

from common.exceptions.exceptions import BadRequestException
from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)


class TestGetPresignedUrlFileUpload(SimpleTestCase):
    """TestCase for get presigned url for file upload"""

    def setUp(self):
        self.service = FileManagementServiceImpl()
        self.service.create_presigned_url_upload_file_uc = MagicMock()
        self.service.repository = MagicMock()

    def test_get_presigned_url_success(self):
        """Test if getting the presigned url for file upload retrieve the url and the fields"""
        mock_response = MagicMock()
        mock_response.to_dict.return_value = {"url": "http://example.com"}
        self.service.create_presigned_url_upload_file_uc.exec.return_value = (
            mock_response
        )

        response = self.service.create_presigned_url_upload_file(
            "FACILITATOR", "test.csv", 1
        )
        self.assertEqual(response, {"url": "http://example.com"})
        self.service.create_presigned_url_upload_file_uc.exec.assert_called_once_with(
            self.service.repository, "test.csv"
        )

    def test_create_presigned_url_failure(self):
        """Test that if the UC returns None a BadRequestException is thrown"""
        self.service.create_presigned_url_upload_file_uc.exec.return_value = None

        with self.assertRaises(BadRequestException):
            self.service.create_presigned_url_upload_file("FACILITATOR", "test.csv", 1)

        self.service.create_presigned_url_upload_file_uc.exec.assert_called_once_with(
            self.service.repository, "test.csv"
        )
