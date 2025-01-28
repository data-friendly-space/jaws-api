"""This module contains the chart model"""

from django.db import models, transaction

from analysis.models.sub_pillar import SubPillar
from common.models import BaseModel


class Chart(models.Model, BaseModel):
    """Model for charts"""
    dataset = models.ForeignKey('file_management.Dataset', on_delete=models.CASCADE)
    created_by = models.ForeignKey('user_management.User', null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    x_col = models.ForeignKey('file_management.ColumnConfiguration', on_delete=models.CASCADE, related_name="x_col")
    y_cols = models.ManyToManyField('file_management.ColumnConfiguration', related_name="y_cols")
    title = models.CharField(max_length=255, null=True)
    x_label = models.CharField(max_length=255, null=True)
    y_label = models.CharField(max_length=255, null=True)
    subpillar = models.ForeignKey('analysis.SubPillar', null=True, on_delete=models.SET_NULL)
    type = models.CharField(
        choices=[("bar", "Bar"), ("line", "Line"), ("pie", "Pie")], default="bar"
    )
    analysis = models.ForeignKey('analysis.Analysis', on_delete=models.CASCADE)

    class Meta:
        """Table's metadata"""
        db_table = "chart"

    @classmethod
    def from_to(cls, chart_to):
        """
        Creates or updates a Chart instance from a ChartTO instance.

        Args:
            chart_to (ChartTO): Transfer Object containing the Chart data.

        Returns:
            Chart: An instance of the Chart model.
        """
        from charts.contract.dto.chart_to import ChartTO
        from file_management.models.column_configuration import ColumnConfiguration
        from user_management.models.user import User
        from file_management.models.dataset import Dataset
        from analysis.models.sub_pillar import SubPillar

        if chart_to is None:
            return None

        if not isinstance(chart_to, ChartTO):
            raise ValueError("The argument must be an instance of ChartTO")

        # Build the defaults dictionary
        defaults = {
            "name": chart_to.name,
            "dataset": Dataset.from_to(chart_to.dataset) if chart_to.dataset else None,
            "created_by": User.from_to(chart_to.createdBy) if chart_to.createdBy else None,
            "created_on": chart_to.createdOn,
            "title": chart_to.title,
            "x_col": ColumnConfiguration.from_to(chart_to.xCol) if chart_to.xCol else None,
            "x_label": chart_to.xLabel,
            "y_label": chart_to.yLabel,
            "subpillar": SubPillar.from_to(chart_to.subpillar) if chart_to.subpillar else None,
            "type": chart_to.type,
        }

        # Remove keys with None values to avoid overwriting
        defaults = {key: value for key, value in defaults.items() if value is not None}

        with transaction.atomic():
            # If chart_to.id exists, fetch the instance or create a new one
            chart_instance, created = cls.objects.update_or_create(
                id=chart_to.id,  # Use `id` to find the object if it exists
                defaults=defaults,
            )

        return chart_instance
