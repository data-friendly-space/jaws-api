"""Contains the chart service"""


from analysis.repository.impl.analysis_repository_impl import AnalysisRepositoryImpl
from analysis.use_cases.get_analysis_by_id_uc import GetAnalysisByIdUC
from charts.repository.impl.chart_repository_impl import ChartRepositoryImpl
from charts.services.chart_service import ChartService
from charts.use_cases.save_chart_uc import SaveChartUC
from common.exceptions.exceptions import NotFoundException
from file_management.repository.file_management_repository_impl import FileManagementRepositoryImpl
from file_management.use_cases.get_dataset_by_id_uc import GetDatasetByIdUC
from file_management.use_cases.get_dataset_columns_uc import GetDatasetColumnsUC


class ChartServiceImpl(ChartService):
    """Chart service"""

    def __init__(self):
        self.save_chart_uc = SaveChartUC.get_instance()
        self.get_dataset_column_uc = GetDatasetColumnsUC.get_instance()
        self.get_dataset_by_id_uc = GetDatasetByIdUC.get_instance()
        self.get_analysis_by_id_uc = GetAnalysisByIdUC.get_instance()
        self.repository = ChartRepositoryImpl()
        self.file_management_repository = FileManagementRepositoryImpl()
        self.analysis_repository = AnalysisRepositoryImpl()

    def save_chart(self, user, config):
        # TODO: Validate if the user can create a chart
        # validate if the dataset exist
        dataset = self.get_dataset_by_id_uc.exec(
            self.file_management_repository, config["dataset_id"]
        )
        if not dataset:
            raise NotFoundException("The dataset doesn't exist")
        # validate if the analysis exist
        analysis = self.get_analysis_by_id_uc.exec(
            self.analysis_repository, config["analysis_id"]
        )
        if not analysis:
            raise NotFoundException("The analysis doesn't exist")

        dataset_columns = self.get_dataset_column_uc.exec(
            self.file_management_repository, config["dataset_id"]
        )
        raw_columns = [col.originalName for col in dataset_columns]
        # validate if the x col exist
        if config["x_col"] not in raw_columns:
            raise NotFoundException(f"The column {config["x_col"]} doesn't exist in the dataset")
        # validate if all the y col exists
        for y_col in config["y_cols"]:
            if y_col not in raw_columns:
                raise NotFoundException(f"The column {y_col} doesn't exist in the dataset")

        new_chart = self.save_chart_uc.exec(
            self.repository, config
        )
        return new_chart.to_dict()
