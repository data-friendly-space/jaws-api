"""Contains the use case for creating a copy of a dataset"""

from pandas import DataFrame
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.s3_put_object_to import S3PutObjectTO
from file_management.contract.repository.file_management_repository import FileManagementRepository


class CreateDatasetCopyUC(BaseUseCase):
    """Singleton use case for creating a copy of a dataset"""
    _instance = None

    def __init__(self):
        if CreateDatasetCopyUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CreateDatasetCopyUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if CreateDatasetCopyUC._instance is None:
            CreateDatasetCopyUC()
        return CreateDatasetCopyUC._instance

    def exec(
            self,
            repository: FileManagementRepository,
            dataframe: DataFrame,
            start_row: int,
            end_row: int,
            values,
            external_identifier: str,
        ) -> S3PutObjectTO:
        new_values_df = DataFrame.from_dict(values)
        dataframe.iloc[start_row - 1 : end_row] = new_values_df[start_row - 1 : end_row].values
        updated_dataframe_csv = dataframe.to_csv(index=False)
        dataset_file_copy = repository.create_dataset_file_copy(
            external_identifier, updated_dataframe_csv
        )
        return dataset_file_copy
