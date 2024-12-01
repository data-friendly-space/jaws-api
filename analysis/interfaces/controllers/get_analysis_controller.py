from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.exceptions.exceptions import InternalServerErrorException
from common.helpers.api_responses import api_response_success, api_response_error


@api_view(["GET"])
def get_analysis_controller(request):
    """
    List all analysis of the user and return them in AnalysisTO format.
    """
    service = AnalysisServiceImpl()
    try:
        return api_response_success("Success", service.get_analysis(), status.HTTP_200_OK)
    except Exception as e:
        return InternalServerErrorException(str(e), [])
