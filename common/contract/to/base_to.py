import dataclasses
from abc import ABC, abstractmethod
from dataclasses import asdict, fields
from typing import Dict, TypeVar, Type, List, Any, get_args, get_origin, Union

T = TypeVar("T", bound="BaseTO")


class BaseTO(ABC):
    @abstractmethod
    def from_model(cls, instance):
        pass

    @classmethod
    def from_models(cls: Type[T], models: List[Any]) -> List[T]:
        """
        Transform a list of model instances into a list of TO instances.
        """
        if not models:
            return []
        return [cls.from_model(model) for model in models]

    def to_dict(self) -> Dict:
        """Return a dict representation of the object."""
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: Dict) -> T:
        """
        Creates a TO instance from a dictionary, including nested TO mappings.

        Args:
            data (Dict): Dictionary with the TO fields.

        Returns:
            T: An instance of the Transfer Object.
        """
        if not data:
            return None

        # Get the field names and types for the class
        field_names = {f.name: f for f in fields(cls)}

        # Process data for the fields in the class
        processed_data = {}
        for key, value in data.items():
            if key in field_names:
                field = field_names[key]
                field_type = field.type

                # Handle UnionType (e.g., int | None)
                origin = get_origin(field_type)
                args = get_args(field_type)

                try:
                    # Check if the field type is a BaseTO or a list of BaseTOs
                    if isinstance(value, dict) and (
                            origin is None and issubclass(field_type, BaseTO)  # Normal BaseTO
                            or origin is Union and any(issubclass(arg, BaseTO) for arg in args)  # UnionType with BaseTO
                    ):
                        # Map the nested object to the TO
                        to_class = field_type if origin is None else next(
                            arg for arg in args if issubclass(arg, BaseTO))
                        processed_data[key] = to_class.from_dict(value)
                    elif (
                            isinstance(value, list) and
                            hasattr(field_type, '__args__') and
                            issubclass(field_type.__args__[0], BaseTO)
                    ):
                        # Map a list of nested TOs
                        processed_data[key] = [field_type.__args__[0].from_dict(item) for item in value]
                    else:
                        # Handle non-dict and non-nested values directly
                        processed_data[key] = value
                except TypeError:
                    # If the field is not a BaseTO, leave the value as-is
                    processed_data[key] = value

        # Fill missing fields with default values
        for f in field_names.values():
            if f.name not in processed_data:
                processed_data[f.name] = f.default if f.default != dataclasses.MISSING else None

        return cls(**processed_data)
