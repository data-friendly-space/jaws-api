from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["GET"])
def get_entriess_controller(request, analysis_id):
    """
    List all entriess of the user and return them in IssueTO format.
    """
    service = AnalysisServiceImpl()
    entriess = service.get_entries_by_analysis_id(analysis_id)
    return api_response_success("Entries retrieved successfully", entriess, status.HTTP_200_OK)
