from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Dict, TypeVar, Type

TModel = TypeVar("TModel")


class BaseTO(ABC):
    model_class: Type[TModel] = None

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

    def to_model(self):
        """
        Transform the TO instance into a model instance.
        """
        if not self.model_class:
            raise NotImplementedError("Derived classes must define a 'model_class' attribute.")

        # Extract data from the TO instance
        model_data = asdict(self)

        # Check for an `id` field to decide between update or create
        if "id" in model_data and model_data["id"] is not None:
            # Update existing model
            model_instance = self.model_class.objects.filter(id=model_data["id"]).first()
            if model_instance:
                for field, value in model_data.items():
                    setattr(model_instance, field, value)
                model_instance.save()
                return model_instance

        # Create new model instance
        return self.model_class.objects.create(**model_data)
