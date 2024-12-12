"""This module contains the controller for putting the scope of an analysis"""

from rest_framework import status
from rest_framework.decorators import api_view

from analysis.contract.io.update_analysis import UpdateAnalysisIn

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data


@api_view(["PUT"])
def put_analysis_scope_controller(request, analysis_id):
    """Update the analysis's scope"""
    service = AnalysisServiceImpl()
    update_analysis_in = UpdateAnalysisIn(data=to_snake_case_data(request.data))

    analysis_updated = service.put_analysis_scope(update_analysis_in, analysis_id, request.user.id)

    return api_response_success(
        data=analysis_updated,
        status_code=status.HTTP_200_OK,
    )
