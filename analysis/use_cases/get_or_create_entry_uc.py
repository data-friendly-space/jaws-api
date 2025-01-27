from analysis.contract.to.entry_to import EntryTO
from analysis.repository.analysis_repository import AnalysisRepository
from common.use_case.base_use_case import BaseUseCase


class GetOrCreateEntryUC(BaseUseCase):
    _instance = None

    def __init__(self):
        if GetOrCreateEntryUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetOrCreateEntryUC._instance = self

    @staticmethod
    def get_instance():
        if GetOrCreateEntryUC._instance is None:
            GetOrCreateEntryUC()
        return GetOrCreateEntryUC._instance

    def exec(self, repository: AnalysisRepository, entry_to: EntryTO) -> EntryTO:
        return repository.get_or_create_entry(entry_to)
