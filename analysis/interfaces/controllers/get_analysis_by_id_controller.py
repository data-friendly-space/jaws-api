from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from app.core.api_response import api_response


@api_view(["GET"])
def get_analysis_by_id_controller(request, id):
    """
    List all analysis of the user and return them in AnalysisTO format.
    """
    service = AnalysisServiceImpl()
    try:
        return api_response("Some Analysis", service.get_analysis_by_id(id), status.HTTP_200_OK)
    except Exception as e:
        return api_response(str(e), [], status.HTTP_500_INTERNAL_SERVER_ERROR)