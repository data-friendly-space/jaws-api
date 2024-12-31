"""This module contains the use case attaching a file to an analysis UC"""
from file_management.contract.repository.file_management_repository import FileManagementRepository


class AttachFileToAnalysisUC:
    """Attach a file into an analysis"""
    _instance = None

    def __init__(self):
        if AttachFileToAnalysisUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AttachFileToAnalysisUC._instance = self

    @staticmethod
    def get_instance():
        """Return a single instance of the class"""
        if AttachFileToAnalysisUC._instance is None:
            AttachFileToAnalysisUC()
        return AttachFileToAnalysisUC._instance

    def exec(self, repository: FileManagementRepository, dataset_id: str, analysis_id: int):
        """Execute the use case"""
        return repository.attach_file_to_analysis(dataset_id, analysis_id)
