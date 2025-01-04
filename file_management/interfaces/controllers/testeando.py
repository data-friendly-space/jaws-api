"""Contains the controller for creating a presigned URL for downloading a file"""

import base64
import pandas as pd
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success

from file_management.repository.file_management_repository_impl import FileManagementRepositoryImpl
from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)


@api_view(["POST"])
def testeando(request):
    """Create a presigned URL to download file"""
    service = FileManagementServiceImpl()
    repo = FileManagementRepositoryImpl()
    dataset = repo.get_dataset_file("global_pcodes.csv")

    df = pd.read_csv(dataset['Body'])
    b = base64.b64encode(bytes(dataset['Body'], 'utf-8'))
    base64_str = b.decode('utf-8')
    return api_response_success(data=base64_str)
