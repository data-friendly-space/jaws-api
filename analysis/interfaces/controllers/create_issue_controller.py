from rest_framework import status
from rest_framework.decorators import api_view

from analysis.contract.io.create_issue_in import CreateIssueIn
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["POST"])
def create_issue_controller(request):
    """
    Create and retrieve new issue
    """
    issue_data = CreateIssueIn(data=request.data)
    service = AnalysisServiceImpl()
    return api_response_success("Issue successfully created", service.create_issue(issue_data), status.HTTP_200_OK)
