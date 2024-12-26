"""This module contain the creation analysis controller"""

from rest_framework import status
from rest_framework.decorators import api_view

from analysis.contract.io.create_analysis_in import CreateAnalysisIn
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data


@api_view(["POST"])
def create_analysis_controller(request):
    """Create a new analysis"""
    service = AnalysisServiceImpl()
    create_analysis_in = CreateAnalysisIn(data=to_snake_case_data(request.data))

    return api_response_success(
        "Success",
        service.create_analysis(create_analysis_in, request.user.id),
        status.HTTP_201_CREATED,
    )
