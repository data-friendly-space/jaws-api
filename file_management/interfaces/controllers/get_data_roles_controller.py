"""Contains the controller for getting all the data roles"""
from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_success
from file_management.service.impl.file_management_service_impl import FileManagementServiceImpl

@api_view(["GET"])
def get_data_roles_controller(_):
    """Controller for getting the data types"""
    service = FileManagementServiceImpl()
    data_roles = service.get_data_roles()
    return api_response_success(data=data_roles)
