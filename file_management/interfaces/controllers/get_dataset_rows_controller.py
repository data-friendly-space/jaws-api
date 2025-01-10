"""Contains the controller for getting dataset rows"""
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["GET"])
def get_dataset_rows_controller(request):
    """Retrieve the rows requested from the dataset"""

    dataset_id = request.query_params.get("dataset_id", None)
    if not dataset_id:
        raise BadRequestException("The dataset id is needed.")
    service = FileManagementServiceImpl()
    query_options = QueryOptions.from_request(request)

    rows = service.get_dataset_rows(request.user, dataset_id, query_options)
    return api_response_success(data=rows)
