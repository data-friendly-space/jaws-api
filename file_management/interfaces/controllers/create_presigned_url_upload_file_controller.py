"""Contains the controller for creating a presigned URL"""

from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)


@api_view(["GET"])
def create_presigned_url_upload_file_controller(request):
    """Create a presigned URL to upload files"""

    service = FileManagementServiceImpl()
    filename = request.query_params.get("filename", None)
    analysis_id = request.query_params.get("analysisId", None)
    if not filename:
        raise BadRequestException("The filename is required")
    if not analysis_id:
        raise BadRequestException("The analysis id is required")
    url = service.create_presigned_url_upload_file(request.user, filename)
    return api_response_success(data=url)
