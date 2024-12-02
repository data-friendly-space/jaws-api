from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["POST"])
def create_analysis_controller(request):
    """
    Create a new analysis
    """
    service = AnalysisServiceImpl()
    if request.data.get("startDate"):
        request.data["startDate"] = request.data["startDate"].split("T")[0]
    request.data["endDate"] = request.data["endDate"].split("T")[0]
    return api_response_success("Success", service.create_analysis(request.data), status.HTTP_201_CREATED)