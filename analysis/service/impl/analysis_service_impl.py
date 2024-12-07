import uuid

from rest_framework import status

from analysis.interfaces.serializers.analysis_serializer import AnalysisSerializer
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.repository.analysis_repository_impl import AnalysisRepositoryImpl
from analysis.service.analysis_service import AnalysisService
from common.exceptions.exceptions import BadRequestException, NotFoundException, InternalServerErrorException
from common.helpers.api_responses import api_response_success


class AnalysisServiceImpl(AnalysisService):

    def __init__(self):
        self.repository = AnalysisRepositoryImpl()
        super().__init__()

    def create_analysis(self, scope):
        if scope["disaggregations"]:
            disaggregations = self.get_disaggregations(scope["disaggregations"])
        else:
            disaggregations = []
        sectors = self.get_sectors(scope["sectors"])
        new_id = uuid.uuid4()
        creator_id = "123"  # TODO: Fill with the current user id
        workspace_id = "456"  # TODO: Fill with the corrseponding workspace id
        self.validate_scope_fields(scope, sectors, disaggregations)
        data = {
            "id": new_id,
            "title": scope["title"],
            "objetives": scope["objetives"],
            "start_date": scope["start_date"],
            "end_date": scope["end_date"],
            "creator": creator_id,
            "workspace_id": workspace_id
        }
        return AnalysisSerializer(self.create_analysis_uc.exec(
            self.repository,
            data,
            disaggregations,
            sectors
        )).data

    def put_analysis_scope(self, scope, analysis_id):
        if scope["disaggregations"]:
            disaggregations = self.get_disaggregations(scope["disaggregations"])
        else:
            disaggregations = []
        sectors = self.get_sectors(scope["sectors"])
        self.validate_scope_fields(scope, sectors, disaggregations)
        return AnalysisSerializer(self.put_analysis_scope_uc.exec(
            self.repository,
            data=scope,
            disaggregations=disaggregations,
            sectors=sectors,
            analysis_id=analysis_id)).data

    def validate_scope_fields(self, scope, sectors, disaggregations=None):
        if not all(scope.get(key) for key in ["title", "objetives", "end_date"]) or not sectors:
            raise BadRequestException("Missing field")

        if scope["start_date"] and scope["start_date"] >= scope["end_date"]:
            raise BadRequestException("Start date must be before end date")

    def get_disaggregations(self, disaggregations):
        return Disaggregation.objects.filter(
            pk__in=disaggregations
        )

    def get_sectors(self, sectors):
        return Sector.objects.filter(pk__in=sectors)

    def get_analysis(self):
        return AnalysisSerializer(self.get_analysis_uc.exec(self.repository), many=True).data

    def get_analysis_by_id(self, id):
        analysis = self.get_analysis_by_id_uc.exec(AnalysisRepositoryImpl(), id)
        if not analysis:
            raise NotFoundException("Analysis not found")
        return AnalysisSerializer(analysis).data
