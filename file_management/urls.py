"""This module contains the urls related with analysis stuff"""

from django.urls import path

from file_management.interfaces.controllers.create_presigned_url_download_file_controller import (
    create_presigned_url_download_file_controller,
)
from file_management.interfaces.controllers.create_presigned_url_upload_file_controller import (
    create_presigned_url_upload_file_controller,
)
from file_management.interfaces.controllers.get_analysis_datasets_controller import (
    get_analysis_datasets_controller,
)
from file_management.interfaces.controllers.confirm_dataset_uploaded_controller import (
    confirm_dataset_uploaded_controller,
)
from file_management.interfaces.controllers.get_dataset_columns_controller import (
    get_dataset_columns_controller
)
from file_management.interfaces.controllers.get_dataset_rows_controller import (
    get_dataset_rows_controller
)
from file_management.interfaces.controllers.update_columns_controller import (
    update_columns_controller
)

urlpatterns = [
    path(
        "get-upload-file-url",
        create_presigned_url_upload_file_controller,
        name="get_upload_file_url",
    ),
    path(
        "get-download-file-url",
        create_presigned_url_download_file_controller,
        name="get_download_file_url",
    ),
    path(
        "get-analysis-datasets",
        get_analysis_datasets_controller,
        name="get_analysis_datasets",
    ),
    path(
        "confirm-dataset-uploaded",
        confirm_dataset_uploaded_controller,
        name="confirm_dataset_uploaded",
    ),
    path(
        "get-columns",
        get_dataset_columns_controller,
        name="get_dataset_columns"
    ),
    path(
        "get-rows",
        get_dataset_rows_controller,
        name="get_dataset_rows"
    ),
    path(
        "update-columns",
        update_columns_controller,
        name="update_columns"
    )
]
