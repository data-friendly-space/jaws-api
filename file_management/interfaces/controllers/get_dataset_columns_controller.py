"""Contains the controller for getting the column configurations of a given dataset"""
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["GET"])
def get_dataset_columns_controller(request):
    """Retrieve the column configurations of a dataset"""
    dataset_id = request.query_params.get("dataset_id", None)
    if not dataset_id:
        raise BadRequestException("The dataset id is needed.")
    service = FileManagementServiceImpl()
    columns = service.get_dataset_columns(request.user, dataset_id)
    return api_response_success(data=columns)
