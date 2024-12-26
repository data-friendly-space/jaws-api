"""This module contains the tests for the controllers"""

from django.test import TestCase
from django.urls import reverse

from common.test_utils import create_logged_in_client


class TestGetPresignedUrlFileUpload(TestCase):
    """TestCase for get presigned url for file upload"""

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.url = resolve

    def test_get_presigned_url_file_upload(self):
        """Test if getting the presigned url for file upload retrieve the url and the fields"""
        
