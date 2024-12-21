"""Contains the controller for getting the admin 0 areas"""
from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success

@api_view(["GET"])
def get_administrative_division_controller(request):
    """Retrieve the admin 0 areas"""
    service = AnalysisServiceImpl()
    parent_p_code = request.query_params.get("parent", None)
    administrative_divisions = service.get_administrative_divisions(parent_p_code)
    return api_response_success(
        "Success",
        administrative_divisions,
        status.HTTP_200_OK
    )
