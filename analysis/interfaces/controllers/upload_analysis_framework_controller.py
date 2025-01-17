from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl
from common.exceptions.exceptions import BadRequestException
from common.helpers.api_responses import api_response_success


@api_view(['POST'])
def upload_analysis_framework_controller(request):
    """
    Receives a CSV file and processes it to create AnalysisFramework, Pillar, and SubPillar models.
    """

    service = AnalysisServiceImpl()

    if 'file' not in request.FILES:
        raise BadRequestException("No file provided.")

    file = request.FILES['file']

    # Ensure the file is a CSV
    if not file.name.endswith('.csv'):
        raise BadRequestException("Invalid file type. Only CSV files are accepted.")

    # Process the CSV file
    return api_response_success(
        "File processed and analysis framework created successfully.",
        service.upload_analysis_framework(file), status.HTTP_201_CREATED)
