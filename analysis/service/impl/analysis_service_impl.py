import uuid
from analysis.interfaces.serializers.analysis_serializer import AnalysisSerializer
from analysis.models.disaggregation import Disaggregation
from analysis.models.sector import Sector
from analysis.repository.analysis_repository_impl import AnalysisRepositoryImpl
from analysis.service.analysis_service import AnalysisService


class AnalysisServiceImpl(AnalysisService):

    def __init__(self):
        self.repository = AnalysisRepositoryImpl()
        super().__init__()

    def create_analysis(self, scope):
        if scope["disaggregations"]:
            disaggregations = Disaggregation.objects.filter(
                pk__in=scope["disaggregations"]
            )
        else:
            disaggregations = []
        sectors = Sector.objects.filter(pk__in=scope["sectors"])
        new_id = uuid.uuid4()
        creator_id = "123" #TODO: Fill with the current user id
        workspace_id = "456" #TODO: Fill with the corrseponding workspace id
        self.__validate_scope_fields(scope, sectors, disaggregations)
        data={
            "id": new_id,
            "title": scope["title"],
            "objetives": scope["objetives"],
            "start_date": scope["startDate"],
            "end_date": scope["endDate"],
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
            disaggregations = Disaggregation.objects.filter(
                pk__in=scope["disaggregations"]
            )
        else:
            disaggregations = []
        sectors = Sector.objects.filter(pk__in=scope["sectors"])
        self.__validate_scope_fields(scope, disaggregations, sectors)
        return AnalysisSerializer(self.put_analysis_scope_uc.exec(
            self.repository,
            data=scope,
            disaggregations=disaggregations,
            sectors=sectors,
            analysis_id=analysis_id)).data

    def __validate_scope_fields(self, scope, sectors, disaggregations=None):     
        if not all(scope.get(key) for key in ["title", "objetives", "end_date"]) or not sectors:
            print("some fields are empty", flush=True)
            # TODO: raise BadRequestException
        if scope["start_date"] and scope["start_date"] >= scope["end_date"]:
            print("start_date > end_date", flush=True)
            # TODO: raise BadRequestException

    def get_analysis(self):
        return AnalysisSerializer(self.get_analysis_uc.exec(self.repository), many=True).data

    def get_analysis_by_id(self, id):
        return AnalysisSerializer(self.get_analysis_by_id_uc.exec(AnalysisRepositoryImpl(), id)).data
