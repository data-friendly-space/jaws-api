"""Contains the data type model"""
from django.db import models


class DataType(models.Model):
    """Dataset Data Type model"""
    name = models.CharField(max_length=255)

    class Meta:
        """Table's metadata"""
        db_table = "data_types"

    @classmethod
    def from_to(cls, data_type_to):
        """
        Creates a DataType instance from a DataTypeTO instance without saving it.

        Args:
            data_type_to (DataTypeTO): Transfer Object containing the DataType data.

        Returns:
            DataType: An instance of the DataType model.
        """
        from file_management.contract.dto.data_type_to import DataTypeTO

        if data_type_to is None:
            return None

        if not isinstance(data_type_to, DataTypeTO):
            raise ValueError("The argument must be an instance of DataTypeTO")

        # Create the DataType instance without saving
        data_type_instance = cls(
            id=data_type_to.id,  # Include only if IDs are passed in the TO
            name=data_type_to.name,
        )
        data_type_instance.save()
        return data_type_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]
