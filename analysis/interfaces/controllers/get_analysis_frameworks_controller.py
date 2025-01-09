"""This module contains the get analysis frameworks controller"""
from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions


@api_view(["GET"])
def get_analysis_frameworks_controller(request):
    """
    List all analysis frameworks and return them in lAnalysisFrameworkTO format.
    """
    service = AnalysisServiceImpl()

    return api_response_success("Analysis frameworks retrieved successfully.",
                                service.get_all_analysis_frameworks(None),
                                status.HTTP_200_OK)
