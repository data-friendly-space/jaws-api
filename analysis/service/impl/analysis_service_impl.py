"""Contains the implementation of AnalysisService"""


from analysis.contract.io.create_analysis_in import CreateAnalysisIn
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
from analysis.use_cases.add_location_uc import AddLocationUC
from analysis.use_cases.create_analysis_uc import CreateAnalysisUC
from analysis.use_cases.get_administrative_divisions_uc import GetAdministrativeDivisionsUC, \
    GetAdministrativeDivisionByIdUC
from analysis.use_cases.get_analysis_by_id_uc import GetAnalysisByIdUC
from analysis.use_cases.get_analysis_uc import GetAnalysisUC
from analysis.use_cases.put_analysis_scope_uc import PutAnalysisScopeUC
from analysis.use_cases.remove_location_uc import RemoveLocationUC
from common.exceptions.exceptions import BadRequestException, NotFoundException
from user_management.repository.user_repository_impl import UserRepositoryImpl
from user_management.usecases.get_user_uc_by_filters import GetUserByFiltersUC


class AnalysisServiceImpl(AnalysisService):
    """Implementation of AnalysisService. Contains the business logic"""

    def __init__(self):
        self.create_analysis_uc = CreateAnalysisUC.get_instance()
        self.put_analysis_scope_uc = PutAnalysisScopeUC.get_instance()
        self.get_analysis_uc = GetAnalysisUC.get_instance()
        self.get_analysis_by_id_uc = GetAnalysisByIdUC.get_instance()
        self.get_administrative_divisions_uc = (
            GetAdministrativeDivisionsUC.get_instance()
        )
        self.get_administrative_division_by_id_uc = (
            GetAdministrativeDivisionByIdUC.get_instance()
        )
        self.add_location_uc = AddLocationUC.get_instance()
        self.remove_location_uc = RemoveLocationUC.get_instance()
        self.get_user_by_filter_uc = GetUserByFiltersUC.get_instance()
        self.repository = AnalysisRepositoryImpl()
        self.user_repository = UserRepositoryImpl()

    def create_analysis(self, create_analysis_in: CreateAnalysisIn,creator_id):
        if not self.get_user_by_filter_uc.exec(self.user_repository,id=creator_id):
            raise BadRequestException("Analysis creator doens't exists")
        if not create_analysis_in.is_valid():
            raise BadRequestException(
                "Create analysis request is not valid: ",
                create_analysis_in.errors)
        scope = create_analysis_in.validated_data
        if scope['disaggregations']:
            disaggregations = self.get_disaggregations(scope['disaggregations'])
        else:
            disaggregations = []
        sectors = self.get_sectors(scope['sectors'])
        self.validate_scope_fields(scope, sectors)
        data = {
            "title": scope["title"],
            "objectives": scope["objectives"],
            "start_date": scope["start_date"],
            "end_date": scope["end_date"],
            "creator_id": creator_id,
            "workspace_id": scope['workspace_id'],
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
                not all(scope[key] for key in ["title", "objectives", "end_date"])
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
        administrative_division_to = self.add_location_uc.exec(self.repository, existing_analysis,
                                                               administrative_division)
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
