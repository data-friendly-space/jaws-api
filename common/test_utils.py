"""Contains test utilities"""
from base64 import encode
from io import StringIO
import boto3
from django.contrib.auth import get_user_model
from django.test import Client
from moto import mock_aws
import pandas as pd
from rest_framework_simplejwt.tokens import RefreshToken

from analysis.models.analysis import Analysis
from file_management.models.column_configuration import ColumnConfiguration
from file_management.models.dataset import Dataset
from file_management.models.dataset_column import DatasetColumn
from user_management.models.organization import Organization
from user_management.models.workspace import Workspace

User = get_user_model()


def create_logged_in_client():
    """Create a user and log him in"""
    user = User.objects.create(
        name="TestName",
        lastname="TestLastname",
        email="test@test.com",
        password="testpassword",
    )
    refresh = RefreshToken.for_user(user)
    client = Client()
    client.force_login(user)
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {str(refresh.access_token)}"
    return client, user

def create_test_organization():
    """Create a test organization"""
    organization = Organization.objects.create(name="TestOrganization2")
    return organization

def create_test_workspace(facilitator: User, organization: Organization = None):
    """Create a test workspace with the required organization"""
    if not organization:
        create_test_organization()
    workspace = Workspace.objects.create(
        title="TestWorksp2ace1",
        organization=organization,
        facilitator_id=facilitator.id,
        creator_id=facilitator.id,
    )
    return workspace



def create_test_analysis(
        user: User,
        workspace: Workspace = None,
        organization: Organization = None
):
    """Create all the structure fo an analysis"""
    if not workspace:
        create_test_workspace(user, organization)
    test_analysis = Analysis.objects.create(
        title="TestAnalysis1",
        workspace_id=workspace.id,
        end_date="2024-12-17",
        creator_id=user.id,
    )
    return test_analysis

@mock_aws
def create_test_dataset(
    user: User,
    analysis: Analysis,
    bucket_name = "testbucket",
    filename = "test.csv",
    content = "column1,column2\nvalue1,value2\nvalue3,value4",
    total_rows = 2,
    total_cols = 2) -> tuple[Dataset, str]:
    """Create a test dataset with columns. 
    Attach it to an analysis and create the column configurations
    Assign the given user as the owner"""
    s3 = boto3.client("s3")
    s3.create_bucket(Bucket=bucket_name)
    s3.put_object(Bucket="testbucket", Key=f"datasets/{filename}", Body=content)
    dataset = Dataset.objects.create(
        filename=filename,
        url=f"http://testurl/{filename}",
        uploaded_by=user,
        size_bytes=len(content.encode("utf-8")),
        total_columns=total_cols,
        total_rows=total_rows,
        external_identifier=f"datasets/{filename}"
    )
    csv_data = StringIO(content)
    dataset_df = pd.read_csv(csv_data)
    for column in dataset_df.columns:
        col = DatasetColumn.objects.create(
            original_name=column,
            dataset=dataset
        )
        ColumnConfiguration.objects.create(
            analysis=analysis,
            column=col
        )
    analysis.datasets.add(dataset)
    return dataset, content
