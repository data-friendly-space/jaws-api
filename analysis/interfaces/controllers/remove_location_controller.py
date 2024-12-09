"""Contains the controller for adding a new location into an existing analysis"""
from rest_framework.decorators import api_view
from rest_framework import status

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success

@api_view(["DELETE"])
def remove_location_controller(request, analysis_id, p_code):
    """Remove an existing location from an analysis"""
    service = AnalysisServiceImpl()
    service.remove_location(analysis_id, p_code)
    return api_response_success(status_code=status.HTTP_204_NO_CONTENT)
