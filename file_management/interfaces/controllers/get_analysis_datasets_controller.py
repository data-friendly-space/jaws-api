"""Contains the controller for getting the analysis datasets"""
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["GET"])
def get_analysis_datasets_controller(request):
    """Retrieve the analysis datasets"""
    analysis_id = request.query_params.get("analysis_id", None)
    if not analysis_id:
        raise BadRequestException("The analysis id is required")
    service = FileManagementServiceImpl()
    datasets = service.get_analysis_datasets(request.user, analysis_id)
    return api_response_success(data=datasets)
