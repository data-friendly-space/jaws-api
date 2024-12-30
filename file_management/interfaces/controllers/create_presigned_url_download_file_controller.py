"""Contains the controller for creating a presigned URL for downloading a file"""

from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success

from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)


@api_view(["POST"])
def create_presigned_url_download_file_controller(request):
    """Create a presigned URL to download file"""

    service = FileManagementServiceImpl()
    dataset_id = request.query_params.get("dataset_id", None)
    if not dataset_id:
        raise BadRequestException("The dataset id is required")
    url = service.create_presigned_url_download_file(request.user, dataset_id)
    return api_response_success(data=url)
