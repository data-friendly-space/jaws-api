"""This module contains the base_model model"""

from abc import ABC, abstractmethod


class BaseModel(ABC):

    @abstractmethod
    def from_to(cls, instance):
        """Transform a TO to a Model"""

    @classmethod
    def from_tos(self, TOs):
        """
        Transform a list of  model instances into a list of instances.
        """
        if TOs is None or TOs.count() <= 0:
            return None
        return [self.from_to(TOs) for model in TOs]
