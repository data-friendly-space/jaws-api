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
        Transform a list of Workspace model instances into a list of WorkspaceTO instances.
        """
        if models is None or len(models) <= 0:
            return None
        return [self.from_model(model) for model in models]

    def to_dict(self) -> Dict:
        return asdict(self)
