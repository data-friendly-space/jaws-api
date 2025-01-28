from rest_framework import status
from rest_framework.decorators import api_view

from analysis.contract.io.update_issue_in import UpdateIssueIn
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["PUT"])
def update_issue_controller(request, issue_id: int):
    """
    Update and retrieve new issue
    """
    issue_data = UpdateIssueIn(data=request.data)
    service = AnalysisServiceImpl()
    return api_response_success("Issue updated successfully", service.update_issue(issue_id, issue_data),
                                status.HTTP_200_OK)
