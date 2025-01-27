from rest_framework import status
from rest_framework.decorators import api_view

from analysis.contract.io.create_issue_in import IssueIn
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["PUT"])
def update_issue_controller(request,issue_id:int):
    """
    Update and retrieve new issue
    """
    issue_data = IssueIn(data=request.data)
    service = AnalysisServiceImpl()
    return api_response_success("Issue updated successfully", service.create_issue(issue_id,issue_data), status.HTTP_200_OK)
