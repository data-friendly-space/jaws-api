from rest_framework import status
from rest_framework.decorators import api_view

from analysis.contract.io.issue_in import IssueIn
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["PUT"])
def update_issue_controller(request,issue_id:int):
    """
    Create and retrieve new issue
    """
    issue_data = IssueIn(data=request.data)
    service = AnalysisServiceImpl()
    return api_response_success("Success", service.create_issue(issue_data), status.HTTP_200_OK)
