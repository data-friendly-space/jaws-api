"""Contains the use case for updating dataset rows"""

from pandas import DataFrame
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.repository.file_management_repository import FileManagementRepository


class UpdateRowsUC(BaseUseCase):
    """Singleton use case for updating dataset rows"""
    _instance = None

    def __init__(self):
        if UpdateRowsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UpdateRowsUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if UpdateRowsUC._instance is None:
            UpdateRowsUC()
        return UpdateRowsUC._instance

    def exec(
            self,
            repository: FileManagementRepository,
            analysis_id: int,
            dataframe: DataFrame,
            start_row: int,
            end_row: int,
            values,
            filename: str
        ) -> None:
        new_values_df = DataFrame.from_dict(values)
        dataframe.iloc[start_row - 1 : end_row] = new_values_df[start_row - 1 : end_row].values
        updated_dataframe_csv = dataframe.to_csv(index=False)
        repository.update_dataset(
            analysis_id, filename, updated_dataframe_csv
        )
