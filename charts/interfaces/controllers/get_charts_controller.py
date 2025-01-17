"""Contains the controller for getting the charts of an analysis"""
from rest_framework import status
from rest_framework.decorators import api_view

from charts.services.impl.chart_service_impl import ChartServiceImpl
from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success

@api_view(["GET"])
def get_charts_controller(request):
    """Save a chart"""
    analysis_id = request.query_params.get("analysis_id", None)
    if not analysis_id:
        raise BadRequestException("The analysis id is needed")
    subpillars_raw = request.query_params.get("subpillar_ids", [])
    if subpillars_raw:
        subpillar_ids = subpillars_raw.split(",")
    else:
        subpillar_ids = []
    service = ChartServiceImpl()
    new_chart = service.get_charts(request.user, analysis_id, subpillar_ids)
    return api_response_success(data=new_chart)
