"""This module contains the use case detaching a file from an analysis UC"""
from file_management.contract.repository.file_management_repository import FileManagementRepository


class DetachFileFromAnalysisUC:
    """Detach a file from an analysis"""
    _instance = None

    def __init__(self):
        if DetachFileFromAnalysisUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DetachFileFromAnalysisUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if DetachFileFromAnalysisUC._instance is None:
            DetachFileFromAnalysisUC()
        return DetachFileFromAnalysisUC._instance

    def exec(self, repository: FileManagementRepository, dataset_id: str, analysis_id: int):
        """Execute the use case"""
        return repository.detach_file_from_analysis(dataset_id, analysis_id)
