"""Tests of the urls within analysis"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from file_management.interfaces.controllers.confirm_dataset_uploaded_controller import (
    confirm_dataset_uploaded_controller,
)
from file_management.interfaces.controllers.create_presigned_url_download_file_controller import (
    create_presigned_url_download_file_controller,
)
from file_management.interfaces.controllers.create_presigned_url_upload_file_controller import (
    create_presigned_url_upload_file_controller,
)
from file_management.interfaces.controllers.get_analysis_datasets_controller import (
    get_analysis_datasets_controller,
)
from file_management.interfaces.controllers.get_data_roles_controller import (
    get_data_roles_controller,
)
from file_management.interfaces.controllers.get_data_types_controller import (
    get_data_types_controller,
)
from file_management.interfaces.controllers.get_dataset_columns_controller import (
    get_dataset_columns_controller,
)
from file_management.interfaces.controllers.get_dataset_rows_controller import (
    get_dataset_rows_controller,
)
from file_management.interfaces.controllers.get_merge_preview_controller import get_merge_preview_controller
from file_management.interfaces.controllers.merge_datasets_controller import merge_datasets_controller
from file_management.interfaces.controllers.update_columns_controller import (
    update_columns_controller,
)
from file_management.interfaces.controllers.update_rows_controller import (
    update_rows_controller,
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

    def test_confirm_dataset_uploaded(self):
        """Test that the url for confirming that a dataset was uploaded works"""
        url = reverse("confirm_dataset_uploaded")
        self.assertEqual(resolve(url).func, confirm_dataset_uploaded_controller)

    def test_get_dataset_columns(self):
        """Test that getting the dataset's c
        olumns works"""
        url = reverse("get_dataset_columns")
        self.assertEqual(resolve(url).func, get_dataset_columns_controller)

    def test_get_dataset_rows(self):
        """Test that the url for getting rows of a dataset works"""
        url = reverse("get_dataset_rows")
        self.assertEqual(resolve(url).func, get_dataset_rows_controller)

    def test_update_columns(self):
        """Test that the url for updating the column configurations of a dataset works"""
        url = reverse("update_columns")
        self.assertEqual(resolve(url).func, update_columns_controller)

    def test_update_rows(self):
        """Test that the url for updating the rows of a dataset works"""
        url = reverse("update_rows")
        self.assertEqual(resolve(url).func, update_rows_controller)

    def test_get_data_types(self):
        """Test that the url for getting the data types"""
        url = reverse("get_data_types")
        self.assertEqual(resolve(url).func, get_data_types_controller)

    def test_get_data_roles(self):
        """Test that the url for getting the data roles"""
        url = reverse("get_data_roles")
        self.assertEqual(resolve(url).func, get_data_roles_controller)

    def test_get_merge_preview(self):
        """Test that the url for getting a merge preview works"""
        url = reverse("get_merge_preview")
        self.assertEqual(resolve(url).func, get_merge_preview_controller)

    def test_merge_datasets(self):
        """Test that the url for merging datasets"""
        url = reverse("merge_datasets")
        self.assertEqual(resolve(url).func, merge_datasets_controller)
