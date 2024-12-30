"""Tests of the urls within analysis"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from file_management.interfaces.controllers.create_presigned_url_download_file_controller import (
    create_presigned_url_download_file_controller,
)
from file_management.interfaces.controllers.create_presigned_url_upload_file_controller import (
    create_presigned_url_upload_file_controller,
)
from file_management.interfaces.controllers.get_analysis_datasets_controller import (
    get_analysis_datasets_controller,
)


class TestUrls(SimpleTestCase):
    """Contains the tests of each url's controller"""

    def test_create_presigned_url_upload_files(self):
        """Test that create presigned url for upload files works"""
        url = reverse("get_upload_file_url")
        self.assertEqual(resolve(url).func, create_presigned_url_upload_file_controller)

    def test_create_presigned_url_download_files(self):
        """Test that create presigned url for upload files works"""
        url = reverse("get_download_file_url")
        self.assertEqual(
            resolve(url).func, create_presigned_url_download_file_controller
        )

    def test_get_datasets_by_analysis(self):
        """Test that getting the datasets from an anlysis works"""
        url = reverse("get_analysis_datasets")
        self.assertEqual(resolve(url).func, get_analysis_datasets_controller)
