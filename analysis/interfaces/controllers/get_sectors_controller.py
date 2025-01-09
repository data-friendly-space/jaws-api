"""This module contains the get analysis frameworks controller"""
from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success
from common.helpers.query_options import QueryOptions


@api_view(["GET"])
def get_all_sectors_controller(request):
    """
    List all sectors of return them in SectorTO format.
    """
    service = AnalysisServiceImpl()


    return api_response_success("Sectors retrieved successfully.",
                                service.get_all_sectors(),
                                status.HTTP_200_OK)
