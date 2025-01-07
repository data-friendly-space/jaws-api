"""This module contains the create or update analysis question to an analysis controller"""
from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["PUT"])
def create_or_update_analysis_question_controller(request, analysis_id: int):
    """
    Create or update analysis question to an analysis
    """
    service = AnalysisServiceImpl()
    content = request.data['content']
    return api_response_success("Analysis question create or updated successfully.",
                                service.update_analysis_questions(analysis_id, content),
                                status.HTTP_200_OK)
