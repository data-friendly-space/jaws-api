from abc import abstractmethod


class BaseModel:
    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]

    @abstractmethod
    def from_to(cls, issue_to):
        """Transform a TO instance into a model instance."""
