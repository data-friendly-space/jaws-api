"""Contains the controller to get the analysis steps"""
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success

@api_view(["GET"])
def get_steps_controller(request):
    """Return the analysis steps"""
    service = AnalysisServiceImpl()
    steps = service.get_steps()
    return api_response_success(
        data=steps
    )
