"""Contains the column configuration model"""
from django.db import models


class ColumnConfiguration(models.Model):
    """Dataset Column configuration model"""
    column = models.ForeignKey('file_management.DatasetColumn', on_delete=models.CASCADE)
    include = models.BooleanField(default=True)
    alias = models.CharField(max_length=255, null=True, blank=True)
    data_type = models.ForeignKey('file_management.DataType', null=True, on_delete=models.SET_NULL)
    data_role = models.ForeignKey('file_management.DataRole', null=True, on_delete=models.SET_NULL)
    last_change = models.DateTimeField(auto_now=True)
    subpillar = models.ForeignKey('analysis.SubPillar', null=True, on_delete=models.SET_NULL)
    analysis = models.ForeignKey('analysis.Analysis', on_delete=models.CASCADE)

    class Meta:
        """Table's metadata"""
        db_table = "column_configurations"

    @classmethod
    def from_to(cls, column_config_to):
        """
        Creates a ColumnConfiguration instance from a ColumnConfigurationTO instance without saving it.

        Args:
            column_config_to (ColumnConfigurationTO): Transfer Object containing the ColumnConfiguration data.

        Returns:
            ColumnConfiguration: An instance of the ColumnConfiguration model.
        """
        from analysis.models.sub_pillar import SubPillar
        from file_management.models.dataset_column import DatasetColumn
        from file_management.models.data_type import DataType
        from file_management.models.data_role import DataRole
        from file_management.contract.dto.column_configuration_to import ColumnConfigurationTO

        if column_config_to is None:
            return None

        if not isinstance(column_config_to, ColumnConfigurationTO):
            raise ValueError("The argument must be an instance of ColumnConfigurationTO")

        # Resolve ForeignKey relationships
        column_instance = DatasetColumn.objects.get(
            original_name=column_config_to.originalName) if column_config_to.originalName else None

        # Create the ColumnConfiguration instance without saving
        column_config_instance = cls(
            alias=column_config_to.alias,
            include=column_config_to.include,
            data_type=DataType.from_to(column_config_to.dataType),
            data_role=DataRole.from_to(column_config_to.dataRole),
            subpillar=SubPillar.from_to(column_config_to.subpillar),
            column=column_instance,
        )
        column_config_instance.save()
        return column_config_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]
