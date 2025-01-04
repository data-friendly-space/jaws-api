"""This module contains the tests for the services"""

from unittest.mock import MagicMock
import boto3
from django.test import SimpleTestCase, TestCase

from moto import mock_aws

from analysis.models.analysis import Analysis
from common.constants.constants import DATASET_MAX_SIZE
from common.exceptions.exceptions import BadRequestException, ForbiddenException, NotFoundException
from common.test_utils import create_test_analysis
from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO
from file_management.contract.dto.s3_object_attributes_to import S3ObjectAttributesTO
from file_management.models.column_configuration import ColumnConfiguration
from file_management.models.dataset import Dataset
from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)
from user_management.models.organization import Organization
from user_management.models.role import Role
from user_management.models.user import User
from user_management.models.user_analysis_role import UserAnalysisRole
from user_management.models.workspace import Workspace


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
        self.service.create_presigned_url_upload_file_uc.exec.return_value = presigned_url_mock

        mock_dataset = MagicMock()
        mock_dataset.id = 456

        response = self.service.create_presigned_url_upload_file(
            self.user, self.filename, self.analysis_id
        )

        self.service.create_presigned_url_upload_file_uc.exec.assert_called_once()
        self.assertEqual(response, presigned_url_mock.to_dict())


class TestCreatePresignedUrlDownloadFile(SimpleTestCase):
    """Contains the test cases for creating a presigned url for file downloading"""
    def setUp(self):
        self.service = FileManagementServiceImpl()
        self.service.repository = MagicMock()
        self.service.create_presigned_url_download_file_uc = MagicMock()

    def test_invalid_dataset_id(self):
        """Test that usign a invalid dataset raises a NotFoundException"""
        user = MagicMock()
        user.id = 1
        dataset_id = "12345"

        self.service.repository.get_dataset_by_id.return_value = None
        with self.assertRaises(NotFoundException):
            self.service.create_presigned_url_download_file(user, dataset_id)

    def test_not_response(self):
        """Test that if the response from aws is empty raises a bad request"""
        user = MagicMock()
        user.id = 1
        dataset_id = "12345"

        self.service.create_presigned_url_download_file_uc.exec.return_value = None
        with self.assertRaises(BadRequestException):
            self.service.create_presigned_url_download_file(user, dataset_id)

    def test_success_with_valid_data(self):
        """Test that if the dataset is valid and aws returns something it doesnt fails"""
        user = MagicMock()
        user.id = 1
        dataset_id = "12345"

        self.service.create_presigned_url_download_file_uc.exec.return_value = "https://some-url"

        response = self.service.create_presigned_url_download_file(user, dataset_id)
        self.assertEqual(response, "https://some-url")


class TestGetAnalysisDatasets(TestCase):  # noqa: F821
    """Contains the test cases for getting the datasets of a given analysis"""
    def setUp(self):
        self.service = FileManagementServiceImpl()
        self.user = User.objects.create(
            name="TestName",
            lastname="TestLastname",
            email="test@test.com",
            password="testpassword",
        )
        self.org = Organization.objects.create(name="TestOrganization2")
        self.workspace = Workspace.objects.create(
            title="TestWorksp2ace1",
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
        self.dataset = Dataset.objects.create(
            filename="test.csv",
            url="http://testurl/test.csv",
            uploaded_by=self.user,
            size_bytes=12345,
            total_rows=1,
            total_columns=1
        )
        self.test_analysis.datasets.add(self.dataset)

    def test_invalid_analysis_fails(self):
        """Test that using an invalid analysis id raises an exception"""
        invalid_analysis_id = 12345
        with self.assertRaises(NotFoundException):
            self.service.get_analysis_datasets(self.user, invalid_analysis_id)

    def test_user_not_in_analysis_fails(self):
        """Tests that if the user doesnt belong to the analysis it raises a forbidden exception"""
        with self.assertRaises(ForbiddenException):
            self.service.get_analysis_datasets(self.user, self.test_analysis.id)

    def test_valid_data(self):
        """Test that if the analysis exists and the user belong to it then it return an array with datasets"""
        UserAnalysisRole.objects.create(
            analysis=self.test_analysis,
            user=self.user,
            role=Role.objects.first()
        )
        response = self.service.get_analysis_datasets(self.user, self.test_analysis.id)
        self.assertEqual(response[0]['id'], self.dataset.id)

@mock_aws
class TestConfirmDatasetUploaded(TestCase):
    """Test the method for confirming that a dataset was uploaded"""

    def setUp(self):
        self.service = FileManagementServiceImpl()
        self.service.get_dataset_file_uc = MagicMock()
        self.user = User.objects.create(
            name="TestName",
            lastname="TestLastname",
            email="test@test.com",
            password="testpassword",
        )
        self.analysis = create_test_analysis(self.user)
        self.filename = "test.csv"
        self.analysis_id = 1

        self.s3 = boto3.client("s3")
        self.s3.create_bucket(Bucket="testbucket")
        self.csv_content = "column1,column2\nvalue1,value2\nvalue3,value4"
        self.s3.put_object(Bucket="testbucket", Key=self.filename, Body=self.csv_content)


    def test_dataset_not_found(self):
        """Test that if the dataset was not found it raises a not found exception"""
        self.service.get_dataset_file_uc.exec.return_value = None

        with self.assertRaises(NotFoundException):
            self.service.confirm_dataset_uploaded(
                self.user,
                self.filename,
                self.analysis_id
            )
        self.service.get_dataset_file_uc.exec.assert_called_once()

    def test_size_bytes_too_big(self):
        """Test that if the dataset size is too big it raises a bad request"""
        self.service.get_dataset_file_uc.exec.return_value = S3ObjectAttributesTO.from_model(
            self.s3.get_object(
                Bucket="testbucket", Key=self.filename
            )
        )
        self.service.get_dataset_file_uc.exec.return_value.ContentLength = DATASET_MAX_SIZE + 1


        with self.assertRaises(BadRequestException):
            self.service.confirm_dataset_uploaded(
                self.user,
                self.filename,
                self.analysis_id
            )
        self.service.get_dataset_file_uc.exec.assert_called_once()

    @mock_aws
    def test_valid_size_and_dataset(self):
        """Test that with valid size and dataset it create the dataset, the column configurations and attach the dataset to the analysis, returning the column configurations"""
        self.service.get_dataset_file_uc.exec.return_value = S3ObjectAttributesTO.from_model(
            self.s3.get_object(
                Bucket="testbucket", Key=self.filename
            )
        )

        response = self.service.confirm_dataset_uploaded(self.user, self.filename, self.analysis.id)

        dataset = Dataset.objects.first()

        column_configurations = ColumnConfiguration.objects.all()

        self.assertEqual(dataset.filename, self.filename)
        self.assertEqual(self.analysis.datasets.first(), dataset)
        self.assertEqual(len(column_configurations), 2)

        column_configuration_to = ColumnConfigurationTO.from_models(column_configurations)
        column_configurations_dict = [col.to_dict() for col in column_configuration_to]
        self.assertEqual(column_configurations_dict, response)

        self.assertEqual(dataset.total_columns, 2)
        self.assertEqual(dataset.total_rows, 2)
