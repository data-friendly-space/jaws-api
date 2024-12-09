"""This module contains the get analysis controller"""
from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["GET"])
def get_analysis_controller(request):
    """
    List all analysis of the user and return them in AnalysisTO format.
    """
    service = AnalysisServiceImpl()

    return api_response_success("Success",
                                service.get_analysis(),
                                status.HTTP_200_OK)
