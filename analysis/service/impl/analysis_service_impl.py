"""Contains the implementation of AnalysisService"""

import uuid


from analysis.interfaces.serializers.administrative_division_serializer import (
    AdministrativeDivisionSerializer,
)
from analysis.interfaces.serializers.analysis_serializer import AnalysisSerializer
from analysis.models.administrative_division import AdministrativeDivision
from analysis.models.analysis import Analysis
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.repository.analysis_repository_impl import AnalysisRepositoryImpl
from analysis.service.analysis_service import AnalysisService
from common.exceptions.exceptions import BadRequestException, NotFoundException


class AnalysisServiceImpl(AnalysisService):
    """Implementation of AnalysisService. Contains the business logic"""

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
        self.validate_scope_fields(scope, sectors)
        data = {
            "id": new_id,
            "title": scope["title"],
            "objetives": scope["objetives"],
            "start_date": scope["start_date"],
            "end_date": scope["end_date"],
            "creator": creator_id,
            "workspace_id": workspace_id,
        }
        return AnalysisSerializer(
            self.create_analysis_uc.exec(
                self.repository, data, disaggregations, sectors
            )
        ).data

    def put_analysis_scope(self, scope, analysis_id):
        if scope["disaggregations"]:
            disaggregations = self.get_disaggregations(scope["disaggregations"])
        else:
            disaggregations = []
        sectors = self.get_sectors(scope["sectors"])
        self.validate_scope_fields(scope, sectors)
        return AnalysisSerializer(
            self.put_analysis_scope_uc.exec(
                self.repository,
                data=scope,
                disaggregations=disaggregations,
                sectors=sectors,
                analysis_id=analysis_id,
            )
        ).data

    def validate_scope_fields(self, scope, sectors):
        """Validate that the scope contains everything needed and the sectors are not empty"""
        if (
            not all(scope.get(key) for key in ["title", "objetives", "end_date"])
            or not sectors
        ):
            raise BadRequestException("Missing field")

        if scope["start_date"] and scope["start_date"] >= scope["end_date"]:
            raise BadRequestException("Start date must be before end date")

    def get_disaggregations(self, disaggregations):
        """Retrieve the disaggregations"""
        return Disaggregation.objects.filter(pk__in=disaggregations)

    def get_sectors(self, sectors):
        """Retrieve the sectors"""
        return Sector.objects.filter(pk__in=sectors)

    def get_analysis(self):
        return AnalysisSerializer(
            self.get_analysis_uc.exec(self.repository), many=True
        ).data

    def get_analysis_by_id(self, analysis_id):
        analysis = self.get_analysis_by_id_uc.exec(
            self.repository, analysis_id
        )
        if not analysis:
            raise NotFoundException("Analysis not found")
        return AnalysisSerializer(analysis).data

    def get_administrative_divisions(self, parent_p_code):
        administrative_divisions = self.get_administrative_divisions_uc.exec(
            self.repository, parent_p_code
        )
        if not administrative_divisions:
            raise NotFoundException("Administrative divisions not found")
        return AdministrativeDivisionSerializer(
            administrative_divisions, many=True
        ).data

    def add_location(self, analysis_id, p_code):
        administrative_division = AdministrativeDivision.objects.filter(p_code=p_code).first()
        if not administrative_division:
            raise NotFoundException("Administrative division not found")
        existing_analysis = Analysis.objects.filter(id=analysis_id).first()
        if not existing_analysis:
            raise NotFoundException("Analysis not found")
        if existing_analysis.locations.filter(p_code=p_code).exists():
            raise BadRequestException("The location is already in the analysis")
        administrative_division_to = self.add_location_uc.exec(self.repository, existing_analysis, administrative_division)
        return AdministrativeDivisionSerializer(administrative_division_to).data

    def remove_location(self, analysis_id, p_code):
        administrative_division = AdministrativeDivision.objects.filter(p_code=p_code).first()
        if not administrative_division:
            raise NotFoundException("Administrative division not found")
        existing_analysis = Analysis.objects.filter(id=analysis_id).first()
        if not existing_analysis:
            raise NotFoundException("Analysis not found")
        if not existing_analysis.locations.filter(p_code=p_code).exists():
            raise BadRequestException("The location is not present in the analysis")
        self.remove_location_uc.exec(self.repository, existing_analysis, administrative_division)
