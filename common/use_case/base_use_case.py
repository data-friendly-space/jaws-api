"""Contains the base class for use cases"""
from abc import ABC, abstractmethod


class BaseUseCase(ABC):
    """Base class for use cases"""
    @abstractmethod
    def exec(self, **kwargs):
        """Execute the use case"""
