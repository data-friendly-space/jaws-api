from abc import ABC, abstractmethod
from dataclasses import asdict, fields, dataclass
from typing import Dict, TypeVar, Type

T = TypeVar("T", bound="BaseTO")


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

    @classmethod
    def from_dict(cls: Type[T], data: Dict) -> T:
        """
        Creates a TO instance from a dictionary.
        Ignores any extra fields that are not part of the TO.

        Args:
            data (Dict): Dictionary with the TO fields.

        Returns:
            T: An instance of the Transfer Object.
        """
        if not data:
            return None

        # Filter out keys that are not part of the TO fields
        field_names = {f.name for f in fields(cls)}
        filtered_data = {key: value for key, value in data.items() if key in field_names}

        # Use default values for missing fields
        return cls(**filtered_data)
