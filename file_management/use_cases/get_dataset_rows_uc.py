"""Contains the use case for getting dataset rows"""

from typing import List
import pandas as pd
from common.helpers.query_options import QueryOptions
from common.use_case.base_use_case import BaseUseCase
from file_management.contract.dto.s3_object_attributes_to import S3ObjectAttributesTO


class GetDatasetRowsUC(BaseUseCase):
    """Singleton use case for getting dataset rows"""
    _instance = None

    def __init__(self):
        if GetDatasetRowsUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetDatasetRowsUC._instance = self

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance"""
        if GetDatasetRowsUC._instance is None:
            GetDatasetRowsUC()
        return GetDatasetRowsUC._instance

    def exec(
            self,
            dataset: S3ObjectAttributesTO,
            query_options: QueryOptions
        ) -> List[dict]:
        try:
            dataset_df = pd.read_csv(dataset.Body)
        except pd.errors.ParserError:
            dataset_df = pd.read_csv(dataset.Body, sep=";")
        rows = query_options.paginate_and_filter_dataframe(dataset_df)
        return rows
