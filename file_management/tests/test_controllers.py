"""This module contains the tests for the controllers"""

from unittest.mock import MagicMock, patch
import boto3
from django.test import TestCase
from django.urls import reverse
from moto import mock_aws
import pandas as pd

from analysis.models.analysis import Analysis
from analysis.models.sub_pillar import SubPillar
from common.exceptions.exceptions import BadRequestException
from common.test_utils import (
    create_logged_in_client,
    create_test_analysis,
    create_test_dataset,
)
from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO
from file_management.models.column_configuration import ColumnConfiguration
from file_management.models.data_role import DataRole
from file_management.models.data_type import DataType
from file_management.models.dataset import Dataset
from file_management.models.dataset_column import DatasetColumn
from user_management.models.organization import Organization
from user_management.models.role import Role
from user_management.models.user_analysis_role import UserAnalysisRole
from user_management.models.workspace import Workspace


REPOSITORY_PATH = (
    "file_management.repository.file_management_repository_impl.bucket_name"
)
TEST_S3_BUCKET_NAME = "testbucket"


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
        mock_service_instance.create_presigned_url_download_file.side_effect = (
            BadRequestException()
        )
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
                "filename": "Prueba3.txt",
            },
            {
                "id": "de98223f-cb5d-4512-88a5-c143c55a2775",
                "uploadedBy": "910c285d-d9a9-4d2c-af4e-31f4fb93a1c4",
                "sizeBytes": 10485760,
                "createdAt": "2024-12-30T17:20:48.556865Z",
                "updatedAt": "2024-12-30T17:20:48.561312Z",
                "mimeType": "text/csv",
                "url": "https://testUrl",
                "filename": "Prueba3.txt",
            },
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
                size_bytes=12345,
                total_columns=1,
                total_rows=1,
            )
        )
        UserAnalysisRole.objects.create(
            user=self.user, analysis=self.analysis, role=Role.objects.first()
        )

    def test_call_without_analysis_id_fails(self):
        """Tests that if the query param analysis_id is not present it raises an exception"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_call_with_valid_data_works(self):
        """Test that if the analysis_id is present and valid works"""
        response = self.client.get(self.url + f"?analysis_id={self.analysis.id}")

        self.assertEqual(response.status_code, 200)


class TestConfirmDatasetUploaded(TestCase):
    """Test the controller for confirming that a dataset was uploaded"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.url = reverse("confirm_dataset_uploaded")
        self.test_analysis = create_test_analysis(self.user)
        self.test_filename = "test.csv"

    def test_missing_filename(self):
        """Test that if the filename is missing the response is a bad request"""
        response = self.client.post(f"{self.url}?analysis_id={self.test_analysis.id}")

        self.assertEqual(response.status_code, 400)

    def test_missing_analysis_id(self):
        """Test that if the analysis id is missing the response is a bad request"""
        response = self.client.post(f"{self.url}?filename={self.test_filename}")

        self.assertEqual(response.status_code, 400)

    @patch(
        "file_management.interfaces.controllers.confirm_dataset_uploaded_controller.FileManagementServiceImpl"
    )
    def test_valid_data(self, mock_service):
        """Test that if the filename and the analysis are present it works"""
        mock_service_instance = MagicMock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.confirm_dataset_uploaded.return_value = {}

        response = self.client.post(
            f"{self.url}?analysis_id={self.test_analysis.id}&filename={self.test_filename}"
        )

        self.assertEqual(response.status_code, 200)


class TestGetDatasetColumns(TestCase):
    """Test the controller for getting a dataset's columns"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.analysis = create_test_analysis(self.user)
        self.dataset, self.dataset_content = create_test_dataset(
            self.user, self.analysis
        )
        self.url = reverse("get_dataset_columns")

    def test_call_without_dataset_id_fails(self):
        """Test that calling the endpoint without a dataset id fails"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_dataset_id_invalid_uuid(self):
        """Test that calling the endpoint with a invalid dataset id fails"""
        invalid_id = "asd"
        response = self.client.get(f"{self.url}?dataset_id={invalid_id}")

        self.assertEqual(response.status_code, 400)

    def test_dataset_id_valid(self):
        """Test that calling the endpoint with a valid dataset id returns the expected response object"""
        response = self.client.get(
            f"{self.url}?dataset_id={self.dataset.id}&analysis_id={self.analysis.id}"
        )
        self.assertEqual(response.status_code, 200)

        column_config_to = ColumnConfigurationTO.from_models(
            ColumnConfiguration.objects.all()
        )
        self.assertEqual(
            response.data["payload"], [col.to_dict() for col in column_config_to]
        )


@mock_aws
@patch(REPOSITORY_PATH, TEST_S3_BUCKET_NAME)
class TestGetDatasetRows(TestCase):
    """Test the endpoint for getting dataset rows"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.analysis = create_test_analysis(self.user)
        self.dataset, self.dataset_content = create_test_dataset(
            self.user, self.analysis
        )
        self.url = reverse("get_dataset_rows")
        self.pagination_options = "page_size=3&page_number=1"

    def test_missing_dataset_id(self):
        """Test that if the dataset id is missing it returns BadRequest"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_id_present(self):
        """Test that if the dataset id is present it works"""
        response = self.client.get(
            f"{self.url}?{self.pagination_options}&dataset_id={self.dataset.id}"
        )
        print(response.data, flush=True)
        self.assertEqual(response.status_code, 200)
        response_body = response.data
        self.assertIn("payload", response_body)
        data = response_body["payload"]
        self.assertIn("totalRows", data)
        self.assertIn("totalColumns", data)
        self.assertEqual(data["totalRows"], self.dataset.total_rows)
        self.assertEqual(data["totalColumns"], self.dataset.total_columns)


class TestUpdateColumns(TestCase):
    """Test the endpoint for updating the column configurations of a dataset"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.analysis = create_test_analysis(self.user)
        self.dataset, self.dataset_content = create_test_dataset(
            self.user, self.analysis
        )
        self.url = reverse("update_columns")
        self.columns = DatasetColumn.objects.all()
        self.column_configurations = ColumnConfiguration.objects.all()
        self.subpillar = SubPillar.objects.create(name="test")

    def test_missing_dataset_id(self):
        """Test that if the dataset is missing it raises a BadRequest"""
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 400)

    def test_bad_request_body(self):
        """Test that if there is a problem with the request body it raises a BadRequest"""
        invalid_body = {}
        valid_url = f"{self.url}?dataset_id={self.dataset.id}"
        response = self.client.put(
            valid_url, invalid_body, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_valid_dataset_and_body(self):
        """
        Test that if the dataset id and the body are correct it modifying the dataset configuration
        """
        valid_body = [
            {
                "id": col.id,
                "alias": "a",
                "dataTypeId": None,
                "dataRoleId": None,
                "include": False,
                "subpillarId": None,
            }
            for col in self.column_configurations
        ]
        url = f"{self.url}?dataset_id={self.dataset.id}"
        response = self.client.put(url, valid_body, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        some_col = self.column_configurations[0]
        some_col.refresh_from_db()
        self.assertEqual(some_col.include, False)
        self.assertEqual(some_col.alias, "a")

    def test_update_column_invalid_combination_role_subpillar(self):
        """Test that if the subpillar is provided but the data role is not content it fails"""
        valid_body = [
            {
                "id": col.id,
                "alias": "a",
                "dataTypeId": None,
                "dataRoleId": DataRole.objects.filter(name="Content").first().id,
                "include": False,
                "subpillarId": self.subpillar.id,
            }
            for col in self.column_configurations
        ]
        url = f"{self.url}?dataset_id={self.dataset.id}"
        response = self.client.put(url, valid_body, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        some_col = self.column_configurations[0]
        some_col.refresh_from_db()
        self.assertEqual(some_col.include, False)
        self.assertEqual(some_col.alias, "a")


@mock_aws()
@patch(REPOSITORY_PATH, TEST_S3_BUCKET_NAME)
class TestUpdateRows(TestCase):
    """Test the endpoint for updating rows"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.analysis = create_test_analysis(self.user)
        self.dataset, self.dataset_content = create_test_dataset(
            self.user, self.analysis
        )
        self.url = reverse("update_rows")

        self.dataset_columns = DatasetColumn.objects.all()
        self.column_configurations = ColumnConfiguration.objects.all()

    def test_dataset_id_missing(self):
        """Test that if the dataset id is missing it raises a BadRequest"""
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, 400)

    def test_invalid_request_body(self):
        """Test that if the request body is invalid it raises a BadRequest"""
        invalid_body = {}
        url = f"{self.url}?dataset_id={self.dataset.id}"
        response = self.client.put(url, invalid_body, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_dataset_id_and_body(self):
        """Test that if the dataset id and the request body are correct it update the rows"""
        valid_data = {
            "rows": {"column1": ["test1", "test2"], "column2": ["test3", "test4"]},
            "analysisId": self.analysis.id,
            "pageSize": 10,
            "pageNumber": 1,
        }
        url = f"{self.url}?dataset_id={self.dataset.id}"
        response = self.client.put(url, valid_data, content_type="application/json")

        # Assert status code 200
        self.assertEqual(response.status_code, 200)

        # Assert that a new file was saved and has the same amount of rows and columns
        s3 = boto3.client("s3")
        file_before = s3.get_object(
            Bucket=TEST_S3_BUCKET_NAME, Key=self.dataset.external_identifier
        )
        df_before = pd.read_csv(file_before["Body"])
        new_dataset_external_identifier = (
            f"datasets/{self.analysis.id}/{self.dataset.filename}"
        )
        file_after = s3.get_object(
            Bucket=TEST_S3_BUCKET_NAME, Key=new_dataset_external_identifier
        )
        df_after = pd.read_csv(file_after["Body"])
        self.assertEqual(len(df_before), len(df_after))
        self.assertEqual(len(df_before.columns), len(df_after.columns))

        # Assert that now there are 2 datasets
        amount_of_datasets = Dataset.objects.count()
        self.assertEqual(amount_of_datasets, 2)

        # Assert that a new dataset record was created and has the correct size in bytes
        new_dataset_record = Dataset.objects.filter(
            external_identifier=new_dataset_external_identifier
        ).first()
        size_bytes = new_dataset_record.size_bytes
        self.assertIsNotNone(new_dataset_record)
        self.assertEqual(file_after["ContentLength"], size_bytes)

        # Assert that the analysis has detached the old dataset and attached the new one
        self.analysis.refresh_from_db()
        self.assertEqual(self.analysis.datasets.count(), 1)
        self.assertEqual(
            self.analysis.datasets.first().external_identifier,
            new_dataset_external_identifier,
        )

        # Assert that new dataset columns were created for the new dataset file
        self.dataset_columns = DatasetColumn.objects.all()
        self.assertEqual(len(self.dataset_columns), 4)

        # Assert that the values of the new dataset are updated
        self.assertEqual(df_after["column1"][0], "test1")
        self.assertEqual(df_after["column1"][1], "test2")
        self.assertEqual(df_after["column2"][0], "test3")
        self.assertEqual(df_after["column2"][1], "test4")


class TestGetDataTypes(TestCase):
    """Test the endpoint for getting the data types"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.url = reverse("get_data_types")
        DataType.objects.all().delete()
        self.data_type_test1 = DataType.objects.create(name="Test data type")
        self.data_type_test2 = DataType.objects.create(name="Test data type")

    def test_get_data_types(self):
        """Test that getting the data types return the types saved in the database"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        self.assertTrue(
            isinstance(response.data["payload"], list), "The response isn't a list"
        )
        self.assertEqual(len(response.data["payload"]), 2)
        self.assertEqual(response.data["payload"][0]["name"], "Test data type")


class TestGetDataRoles(TestCase):
    """Test the endpoint for getting the data roles"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.url = reverse("get_data_roles")
        DataRole.objects.all().delete()
        self.test_data_role1 = DataRole.objects.create(name="Test data role")
        self.test_data_role2 = DataRole.objects.create(name="Test data role")

    def test_get_data_roles(self):
        """Test that getting the data types return the roles saved in the database"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        self.assertTrue(
            isinstance(response.data["payload"], list), "The response isn't a list"
        )
        self.assertEqual(len(response.data["payload"]), 2)
        self.assertEqual(response.data["payload"][0]["name"], "Test data role")


@mock_aws
@patch(REPOSITORY_PATH, TEST_S3_BUCKET_NAME)
class TestGetMergePreview(TestCase):
    """Test the endpoint for getting a merge preview"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.analysis = create_test_analysis(self.user)
        self.dataset, self.dataset_content = create_test_dataset(
            self.user,
            self.analysis,
            content="id,name\n1,John\n2,Alice\n3,Mathew\n4,Andrew",
        )
        self.dataset2, self.dataset_content2 = create_test_dataset(
            self.user,
            self.analysis,
            content="id,city\n1,Boston\n2,New York\n3,Colorado\n5,Miami",
            filename="test2.csv",
        )
        self.url = reverse("get_merge_preview")
        self.valid_body = {
            "analysis_id": self.analysis.id,
            "datasets": [
                {"id": self.dataset.id, "join_column": "id"},
                {"id": self.dataset2.id, "join_column": "id"},
            ],
        }

    def test_invalid_body(self):
        """Test that calling the endpoint with an invalid body raises a BadRequest"""
        invalid_body = {}
        response = self.client.post(
            self.url, invalid_body, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_analysis_id(self):
        """Test that calling the endpoint with an invalid analysis id raises a NotFound"""
        invalid_body = self.valid_body
        invalid_body["analysis_id"] = 123123
        response = self.client.post(
            self.url, invalid_body, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_left_join(self):
        """Test that calling the endpoint with valid data works"""
        response = self.client.post(
            self.url, self.valid_body, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        payload = response.data["payload"]
        self.assertEqual(payload["totalRows"], 4)
        self.assertEqual(payload["totalColumns"], 3)
        dict_data = payload["data"].to_dict()
        self.assertEqual(
            dict_data["name"], {0: "John", 1: "Alice", 2: "Mathew", 3: "Andrew"}
        )
        self.assertEqual(
            dict_data["city"], {0: "Boston", 1: "New York", 2: "Colorado", 3: ""}
        )

    def test_outer_join(self):
        """Test that making the join with the 'outer' method works"""
        outer_join_body = self.valid_body
        outer_join_body["method"] = "outer"
        response = self.client.post(
            self.url, self.valid_body, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        payload = response.data["payload"]
        self.assertEqual(payload["totalRows"], 5)
        self.assertEqual(payload["totalColumns"], 3)
        dict_data = payload["data"].to_dict()
        self.assertEqual(
            dict_data["name"], {0: "John", 1: "Alice", 2: "Mathew", 3: "Andrew", 4: ""}
        )
        self.assertEqual(
            dict_data["city"],
            {0: "Boston", 1: "New York", 2: "Colorado", 3: "", 4: "Miami"},
        )

    def test_inner_join(self):
        """Test that using the 'inner' method works"""
        inner_join_body = self.valid_body
        inner_join_body["method"] = "inner"
        response = self.client.post(
            self.url, self.valid_body, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        payload = response.data["payload"]
        self.assertEqual(payload["totalRows"], 3)
        self.assertEqual(payload["totalColumns"], 3)
        dict_data = payload["data"].to_dict()
        self.assertEqual(
            dict_data["name"], {0: "John", 1: "Alice", 2: "Mathew"}
        )
        self.assertEqual(
            dict_data["city"],
            {0: "Boston", 1: "New York", 2: "Colorado"},
        )

    def test_right_join(self):
        """Test that using the 'inner' method works"""
        right_join_body = self.valid_body
        right_join_body["method"] = "right"
        response = self.client.post(
            self.url, self.valid_body, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        payload = response.data["payload"]
        self.assertEqual(payload["totalRows"], 4)
        self.assertEqual(payload["totalColumns"], 3)
        dict_data = payload["data"].to_dict()
        self.assertEqual(
            dict_data["name"], {0: "John", 1: "Alice", 2: "Mathew", 3: ""}
        )
        self.assertEqual(
            dict_data["city"],
            {0: "Boston", 1: "New York", 2: "Colorado", 3: "Miami"},
        )

@mock_aws
@patch(
    REPOSITORY_PATH, TEST_S3_BUCKET_NAME
)
class TestMergeDatasets(TestCase):
    """Tests for the datasets merging endpoint"""
    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.analysis = create_test_analysis(self.user)
        self.dataset1, _ = create_test_dataset(
            self.user,
            self.analysis,
            content="id,name\n1,John\n2,Alice\n3,Mathew\n4,Andrew")
        self.dataset2, _ = create_test_dataset(
            self.user,
            self.analysis,
            content="id,city\n1,Boston\n2,New York\n3,Colorado\n5,Miami",
            filename="test2.csv",
        )
        self.url = reverse("merge_datasets")

        self.valid_body = {
            "analysis_id": self.analysis.id,
            "datasets": [
                {
                    "id": self.dataset1.id,
                    "join_column": "id"
                },
                {
                    "id": self.dataset2.id,
                    "join_column": "id"
                }
            ],
            "method": "left",
            "output_name": "merged.csv"
        }

    def test_invalid_body(self):
        """Test that if the request body is invalid the endpoint returns a BadRequest"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)

    def test_invalid_analysis_id_fails(self):
        """Test that if the analysis id doesn't exist it raises a NotFound"""
        invalid_analysis_id_body = self.valid_body
        invalid_analysis_id_body["analysis_id"] = 1234
        response = self.client.post(
            self.url,
            invalid_analysis_id_body,
            content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_valid_data_success(self):
        """
        Test that if the analysis id exist and the datasets can be merged
        the new dataset is stored, attached to the analysis and 
        the columns and column configurations are created as well
        """
        response = self.client.post(self.url, self.valid_body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", response.data)
        payload = response.data["payload"]
        self.assertEqual(payload["filename"], self.valid_body["output_name"])
        self.assertEqual(
            payload["externalIdentifier"],
            f"datasets/{self.analysis.id}/{self.valid_body["output_name"]}")

        columns_count = DatasetColumn.objects.count()
        self.assertEqual(columns_count, 7)
        self.assertEqual(self.analysis.datasets.count(), 3)

    def test_existing_dataset_filename_fails(self):
        """Test that if the filename already exists it raises a Bad Request"""
        existing_filename_body = self.valid_body
        existing_filename_body["output_name"] = "test.csv"
        response = self.client.post(
            self.url,
            existing_filename_body,
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
