"""Contains the implementation of the chart repository"""

from analysis.models.analysis import Analysis
from analysis.models.sub_pillar import SubPillar
from charts.contract.dto.chart_to import ChartTO
from charts.models.chart import Chart
from charts.repository.chart_repository import ChartRepository
from file_management.models.column_configuration import ColumnConfiguration
from file_management.models.dataset import Dataset


class ChartRepositoryImpl(ChartRepository):
    """Implementation of the chart repository"""

    def save(self,
            chart_type,
            dataset_id,
            analysis_id,
            name,
            x_col,
            subpillar_id,
            y_cols,
            title,
            x_label,
            y_label,
        ):
        dataset = Dataset.objects.get(id=dataset_id)
        x_col = ColumnConfiguration.objects.filter(
            column__original_name=x_col,
            analysis_id=analysis_id
        ).first()
        y_col_configs = ColumnConfiguration.objects.filter(
            column__original_name__in=y_cols,
            column__dataset=dataset,
            analysis_id=analysis_id
        ).all()
        analysis = Analysis.objects.get(id=analysis_id)
        subpillar = SubPillar.objects.get(id=subpillar_id)
        new_chart = Chart.objects.create(
            type=chart_type,
            dataset=dataset,
            name=name,
            x_col=x_col,
            title=title,
            x_label=x_label,
            y_label=y_label,
            analysis=analysis,
            subpillar=subpillar
        )
        new_chart.y_cols.set(y_col_configs)
        return ChartTO.from_model(new_chart)

    def get(self, analysis_id, subpillar_ids):
        if subpillar_ids:
            charts = Chart.objects.filter(analysis_id=analysis_id, subpillar__id__in=subpillar_ids)
        else:
            charts = Chart.objects.filter(analysis_id=analysis_id)
        return ChartTO.from_models(charts)
