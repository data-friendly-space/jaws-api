"""Contains the controller for saving a chart"""
from rest_framework import status
from rest_framework.decorators import api_view

from charts.contract.requests.save_chart_request import SaveChartRequest
from charts.services.impl.chart_service_impl import ChartServiceImpl
from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data

@api_view(["POST"])
def save_chart_controller(request):
    """Save a chart"""
    data = SaveChartRequest(data=to_snake_case_data(request.data))
    if not data.is_valid():
        raise BadRequestException("Check the payload and try again.", data.errors)
    service = ChartServiceImpl()
    new_chart = service.save_chart(request.user, data.validated_data)
    return api_response_success(data=new_chart, status_code=status.HTTP_201_CREATED)
