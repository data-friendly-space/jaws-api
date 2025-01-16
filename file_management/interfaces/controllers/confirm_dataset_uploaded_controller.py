"""Contains the controller for confirming that a dataset was succesfully uploaded to the storage"""

from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success

from file_management.service.impl.file_management_service_impl import (
    FileManagementServiceImpl,
)


@api_view(["POST"])
def confirm_dataset_uploaded_controller(request):
    """Confirm that a dataset was uploaded correctly and load the column configuration"""
    service = FileManagementServiceImpl()
    filename = request.query_params.get("filename", None)
    analysis_id = request.query_params.get("analysis_id", None)
    if not filename:
        raise BadRequestException("The filename is needed.")
    if not analysis_id:
        raise BadRequestException("The analysis id is needed.")
    columns = service.confirm_dataset_uploaded(request.user, filename, analysis_id)
    return api_response_success(data=columns)
