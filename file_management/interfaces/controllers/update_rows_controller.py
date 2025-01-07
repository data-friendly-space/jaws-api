"""Contains the controller for uploading dataset rows"""
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from file_management.contract.requests.update_rows_in import UpdateRowsIn
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["PUT"])
def update_rows_controller(request):
    """Update the rows of a dataset"""
    dataset_id = request.query_params.get("dataset_id", None)
    if not dataset_id:
        raise BadRequestException("The dataset id is needed.")
    update_rows_in = UpdateRowsIn(data=to_snake_case_data(request.data))
    if not update_rows_in.is_valid():
        raise BadRequestException("Check the payload and try again.")

    service = FileManagementServiceImpl()
    service.update_rows(request.user, dataset_id, update_rows_in)

    return api_response_success()
