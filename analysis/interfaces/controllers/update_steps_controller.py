"""Contains the controller to add steps"""
from rest_framework.decorators import api_view

from analysis.contract.io.update_steps_in import UpdateStepsIn
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.exceptions.exceptions import BadRequestException
from common.serializer.CamelCaseMixin import to_snake_case_data

@api_view(["POST"])
def update_steps_controller(request, analysis_id):
    """Update the steps of an analysis"""
    if not analysis_id:
        raise BadRequestException("The step ID is required")
    service = AnalysisServiceImpl()
    step_ids = UpdateStepsIn(data=to_snake_case_data(request.data))
    service.update_steps(analysis_id, step_ids)
