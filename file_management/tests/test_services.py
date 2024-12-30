"""This module contains the tests for the services"""

from unittest.mock import MagicMock
from django.test import SimpleTestCase

from common.exceptions.exceptions import NotFoundException
from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)


class TestGetPresignedUrlFileUpload(SimpleTestCase):
    """TestCase for get presigned url for file upload"""

    def setUp(self):
        self.service = FileManagementServiceImpl()
        self.service.analysis_service = MagicMock()
        self.service.create_presigned_url_upload_file_uc = MagicMock()
        self.service.attach_file_to_analysis_uc = MagicMock()

        self.user = MagicMock()
        self.user.id = 1

        self.filename = "test_file.csv"
        self.analysis_id = 123

    def test_create_presigned_url_success(self):
        """Test that the create presigned url service works"""
        presigned_url_mock = MagicMock()
        presigned_url_mock.fields.key = "mock_key"
        presigned_url_mock.url = "https://mockurl.com/"
        dataset_mock = MagicMock()
        dataset_mock.id = 123
        self.service.create_presigned_url_upload_file_uc.exec.return_value = (
            presigned_url_mock, dataset_mock
        )

        response = self.service.create_presigned_url_upload_file(
            self.user, self.filename, self.analysis_id
        )

        self.service.analysis_service.get_analysis_by_id.assert_called_once_with(
            self.analysis_id
        )
        self.service.create_presigned_url_upload_file_uc.exec.assert_called_once()
        self.service.attach_file_to_analysis_uc.exec.assert_called_once_with(
            self.service.repository, dataset_mock.id, self.analysis_id
        )
        self.assertEqual(response, presigned_url_mock.to_dict())

    def test_analysis_not_found(self):
        """Test that if the analysis was not found a not found exception is raised"""
        self.service.analysis_service.get_analysis_by_id.side_effect = (
            NotFoundException()
        )

        with self.assertRaises(NotFoundException):
            self.service.create_presigned_url_upload_file(
                self.user, self.filename, self.analysis_id
            )
