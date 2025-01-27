"""This module contains the chart model"""

from django.db import models


class Chart(models.Model):
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
        Creates a Chart instance from a ChartTO instance without saving it.

        Args:
            chart_to (ChartTO): Transfer Object containing the Chart data.

        Returns:
            Chart: An instance of the Chart model.
        """
        from charts.contract.dto.chart_to import ChartTO
        from file_management.models.column_configuration import ColumnConfiguration
        from user_management.models.user import User
        from file_management.models.dataset import Dataset
        if chart_to is None:
            return None

        if not isinstance(chart_to, ChartTO):
            raise ValueError("The argument must be an instance of ChartTO")

        # Create the Chart instance without saving
        chart_instance = cls(
            id=chart_to.id,  # Include only if IDs are passed in the TO
            name=chart_to.name,
            dataset=Dataset.from_to(chart_to.dataset),
            created_by=User.from_to(chart_to.createdBy),
            created_on=chart_to.createdOn,
            title=chart_to.title,
            x_col=ColumnConfiguration.from_to(chart_to.xCol),
            x_label=chart_to.xLabel,
            y_label=chart_to.yLabel,
            subpillar=Dataset.from_to(chart_to.dataset),
            type=chart_to.type,
        )
        chart_instance.save()

        return chart_instance

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]
