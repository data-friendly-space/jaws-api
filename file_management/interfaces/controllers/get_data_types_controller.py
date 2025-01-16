"""Contains the controller for getting all the data types"""
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["GET"])
def get_data_types_controller(_):
    """Controller for getting the data types"""
    service = FileManagementServiceImpl()
    data_types = service.get_data_types()
    return api_response_success(data=data_types)
