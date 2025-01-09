"""This module contains the Assign or update analysis frameworks to an analysis controller"""
from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["PUT"])
def assign_or_update_analysis_framework_controller(request, analysis_id: int, analysis_framework_id: int):
    """
    Assign or update analysis frameworks to an analysis
    """
    service = AnalysisServiceImpl()

    return api_response_success("Analysis framework assigned or updated successfully.",
                                service.update_analysis_framework(analysis_id, analysis_framework_id),
                                status.HTTP_200_OK)
