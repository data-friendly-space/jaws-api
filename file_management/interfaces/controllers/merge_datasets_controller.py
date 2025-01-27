"""Contains the controller for merging datasets"""
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from file_management.contract.requests.merge_configuration_in import MergeConfigurationIn
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["POST"])
def merge_datasets_controller(request):
    """Retrieve preview rows of the final dataset"""
    merge_config = MergeConfigurationIn(data=to_snake_case_data(request.data))
    if not merge_config.is_valid():
        raise BadRequestException("Check the payload", merge_config.errors)
    service = FileManagementServiceImpl()
    merge_result = service.merge_datasets(request.user, merge_config.validated_data)
    return api_response_success(data=merge_result)
