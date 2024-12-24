"""Tests of the urls within analysis"""

from django.test import SimpleTestCase
from django.urls import reverse, resolve

from file_management.interfaces.controllers.create_presigned_url_upload_file_controller import (
    create_presigned_url_upload_file_controller,
)


class TestUrls(SimpleTestCase):
    """Contains the tests of each url's controller"""

    def test_create_presigned_url_upload_files(self):
        """Test that create presigned url for upload files works"""
        url = reverse("get_upload_file_url")
        self.assertEqual(resolve(url).func, create_presigned_url_upload_file_controller)
