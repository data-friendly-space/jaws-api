from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["GET"])
def get_analysis_by_id_controller(request, id):
    """
    List all analysis of the user and return them in AnalysisTO format.
    """
    service = AnalysisServiceImpl()
    analysis = service.get_analysis_by_id(id)
    return api_response_success("Success", analysis, status.HTTP_200_OK)
