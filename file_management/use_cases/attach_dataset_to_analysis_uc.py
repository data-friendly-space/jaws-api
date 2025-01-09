"""Contains the use case for getting the administrative divisions"""
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class AttachDatasetToAnalysisUC(BaseUseCase):
    """Singleton use case for getting the administrative divisions"""
    _instance = None

    def __init__(self):
        if AttachDatasetToAnalysisUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AttachDatasetToAnalysisUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if AttachDatasetToAnalysisUC._instance is None:
            AttachDatasetToAnalysisUC()
        return AttachDatasetToAnalysisUC._instance

    def exec(self, repository: AnalysisRepository, analysis_id: int, dataset_id):
        dataset_id = repository.store_dataset(analysis_id, dataset_id)
        return dataset_id
