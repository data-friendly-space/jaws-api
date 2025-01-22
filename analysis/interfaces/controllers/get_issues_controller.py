from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["GET"])
def get_issues_controller(request, analysis_id):
    """
    List all issues of the user and return them in IssueTO format.
    """
    service = AnalysisServiceImpl()
    issues = service.get_issues_by_analysis_id(analysis_id)
    return api_response_success("Success", issues, status.HTTP_200_OK)
