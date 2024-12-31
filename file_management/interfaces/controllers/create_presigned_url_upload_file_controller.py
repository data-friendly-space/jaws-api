"""Contains the controller for creating a presigned URL"""

from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from file_management.contract.io.create_presigned_url_upload_file_in import (
    CreatePresignedUrlUploadFileIn,
)
from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)


@api_view(["POST"])
def create_presigned_url_upload_file_controller(request):
    """Create a presigned URL to upload files"""

    service = FileManagementServiceImpl()
    data = CreatePresignedUrlUploadFileIn(data=to_snake_case_data(request.data))
    if not data or not data.is_valid():
        raise BadRequestException("All fields are required")
    filename = data.validated_data["filename"]
    analysis_id = data.validated_data["analysis_id"]
    size_bytes = data.validated_data["size_bytes"]
    url = service.create_presigned_url_upload_file(request.user, filename, analysis_id, size_bytes)
    return api_response_success(data=url)
