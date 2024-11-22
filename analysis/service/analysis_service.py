from abc import ABC, abstractmethod


class AnalysisService(ABC):
    @abstractmethod
    def put_analysis_scope(self):
        pass
