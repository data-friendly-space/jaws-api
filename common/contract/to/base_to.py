from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Dict


class BaseTO(ABC):
    @abstractmethod
    def from_model(cls, instance):
        pass

    @classmethod
    def from_models(self, models):
        """
        Transform a list of  model instances into a list of instances.
        """
        if models is None or len(models) <= 0:
            return None
        return [self.from_model(model) for model in models]

    def to_dict(self) -> Dict:
        """Return a dict of the object"""
        return asdict(self)

