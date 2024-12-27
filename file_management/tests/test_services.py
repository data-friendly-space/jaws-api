"""This module contains the tests for the services"""

from unittest.mock import MagicMock
from django.test import SimpleTestCase

from common.exceptions.exceptions import BadRequestException, NotFoundException
from file_management.contract.dto.s3_presigned_url_to import S3PresignedUrlTO
from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)


class TestGetPresignedUrlFileUpload(SimpleTestCase):
    """TestCase for get presigned url for file upload"""

    def setUp(self):
        self.service = FileManagementServiceImpl()
        self.service.analysis_service = MagicMock()
        self.service.create_presigned_url_upload_file_uc = MagicMock()
        self.service.create_dataset_uc = MagicMock()
        self.service.attach_file_to_analysis_uc = MagicMock()

        self.user = MagicMock()
        self.user.id = 1

        self.filename = "test_file.csv"
        self.analysis_id = 123

    def test_create_presigned_url_success(self):
        """Test that the create presigned url service works"""
        mock_response = MagicMock()
        mock_response.fields.key = "mock_key"
        mock_response.url = "https://mockurl.com/"
        self.service.create_presigned_url_upload_file_uc.exec.return_value = (
            mock_response
        )

        mock_dataset = MagicMock()
        mock_dataset.id = 456
        self.service.create_dataset_uc.exec.return_value = mock_dataset

        response = self.service.create_presigned_url_upload_file(
            self.user, self.filename, self.analysis_id
        )

        self.service.analysis_service.get_analysis_by_id.assert_called_once_with(
            self.analysis_id
        )
        self.service.create_presigned_url_upload_file_uc.exec.assert_called_once()
        self.service.create_dataset_uc.exec.assert_called_once()
        self.service.attach_file_to_analysis_uc.exec.assert_called_once_with(
            self.service.repository, mock_dataset.id, self.analysis_id
        )
        self.assertEqual(response, mock_response.to_dict())

    def test_analysis_not_found(self):
        """Test that if the analysis was not found a not found exception is raised"""
        self.service.analysis_service.get_analysis_by_id.side_effect = (
            NotFoundException()
        )

        with self.assertRaises(NotFoundException):
            self.service.create_presigned_url_upload_file(
                self.user, self.filename, self.analysis_id
            )

    def test_bad_request_exception(self):
        """Tests that if the response from"""
        self.service.create_presigned_url_upload_file_uc.exec.return_value = None

        with self.assertRaises(BadRequestException):
            self.service.create_presigned_url_upload_file(
                self.user, self.filename, self.analysis_id
            )
