from abc import ABC, abstractmethod

from analysis.contract.repository.base_repository import BaseRepository


class BaseUseCase(ABC):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @abstractmethod
    def exec(self):
        pass