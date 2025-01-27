"""Contains the controller for getting the merge preview"""
from rest_framework.decorators import api_view

from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data
from file_management.contract.requests.merge_configuration_in import MergePreviewConfigurationIn
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["POST"])
def get_merge_preview_controller(request):
    """Merge the datasets and retrieve the new record"""
    merge_config = MergePreviewConfigurationIn(data=to_snake_case_data(request.data))
    if not merge_config.is_valid():
        raise BadRequestException("Check the payload", merge_config.errors)
    service = FileManagementServiceImpl()
    merge_result = service.get_merge_preview(request.user, merge_config.validated_data)
    return api_response_success(data=merge_result)
