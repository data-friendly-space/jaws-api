"""Contains the controller for updating the dataset's columns"""
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from file_management.contract.requests.update_columns_in import ColumnIn
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["PUT"])
def update_columns_controller(request):
    """Update the columns of a dataset"""
    dataset_id = request.query_params.get("dataset_id", None)
    if not dataset_id:
        raise BadRequestException("The dataset id is needed.")
    columns = ColumnIn(data=to_snake_case_data(request.data), many=True)
    if not columns.is_valid():
        raise BadRequestException("Check the payload and try again.")
    service = FileManagementServiceImpl()
    service.update_columns(request.user, dataset_id, columns)

    return api_response_success()
