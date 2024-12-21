"""Contains the controller to add steps"""

from rest_framework.decorators import api_view

from analysis.contract.io.update_steps_in import UpdateStepsIn
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success
from common.serializer.CamelCaseMixin import to_snake_case_data


@api_view(["PUT"])
def update_steps_controller(request, analysis_id):
    """Update the steps of an analysis"""
    # TODO: validate that the user has modify permission to this step
    if not analysis_id:
        raise BadRequestException("The step ID is required")
    service = AnalysisServiceImpl()
    data = UpdateStepsIn(data=to_snake_case_data(request.data))
    if not data.is_valid():
        raise BadRequestException(
            "The steps were not given correctly, please check your input and try again"
        )
    steps = data.validated_data["step_ids"]
    service.update_steps(analysis_id, steps)
    return api_response_success()
