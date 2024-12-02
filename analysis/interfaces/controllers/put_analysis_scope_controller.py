from rest_framework import status
from rest_framework.decorators import api_view

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.helpers.api_responses import api_response_success


@api_view(["PUT"])
def put_analysis_scope_controller(request, id):
    """
    Update the analysis's scope
    """
    service = AnalysisServiceImpl()
    if request.data.get("startDate"):
        request.data["startDate"] = request.data["startDate"].split("T")[0]
    request.data["endDate"] = request.data["endDate"].split("T")[0]

    analysis = {
        "id": id,
        "title": request.data.get("title"),
        "start_date": request.data.get("startDate"),
        "end_date": request.data.get("endDate"),
        "disaggregations": request.data.get("disaggregations"),
        "objetives": request.data.get("objetives"),
        "sectors": request.data.get("sectors"),
    }
    return api_response_success("", service.put_analysis_scope(analysis, id), status.HTTP_201_CREATED)
