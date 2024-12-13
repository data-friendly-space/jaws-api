"""This module contains the get analysis controller"""
from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions


@api_view(["GET"])
def get_analysis_controller(request, workspace_id):
    """
    List all analysis of the user and return them in AnalysisTO format.
    """
    service = AnalysisServiceImpl()

    query_options = QueryOptions.from_request(request)

    return api_response_success("Success",
                                service.get_analysis(workspace_id, query_options),
                                status.HTTP_200_OK)
