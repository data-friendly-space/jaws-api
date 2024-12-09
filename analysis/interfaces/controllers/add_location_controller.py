'''Contains the controller for adding a new location into an existing analysis'''
from rest_framework.decorators import api_view
from rest_framework import status

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success

@api_view(["PUT"])
def add_location_controller(request, analysis_id, p_code):
    '''Appends a new location into an analysis'''
    service = AnalysisServiceImpl()
    return api_response_success(
        data=service.add_location(analysis_id, p_code),
        status_code=status.HTTP_201_CREATED
    )
