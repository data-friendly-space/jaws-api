from abc import ABC, abstractmethod


class BaseUseCase(ABC):
    @abstractmethod
    def exec(self, *args):
        pass
