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
from file_management.interfaces.controllers.get_data_roles_controller import (
    get_data_roles_controller,
)
from file_management.interfaces.controllers.get_data_types_controller import (
    get_data_types_controller,
)
from file_management.interfaces.controllers.get_dataset_columns_controller import (
    get_dataset_columns_controller,
)
from file_management.interfaces.controllers.get_dataset_rows_controller import (
    get_dataset_rows_controller,
)
from file_management.interfaces.controllers.get_merge_preview_controller import (
    get_merge_preview_controller,
)
from file_management.interfaces.controllers.merge_datasets_controller import (
    merge_datasets_controller,
)
from file_management.interfaces.controllers.update_columns_controller import (
    update_columns_controller,
)
from file_management.interfaces.controllers.update_rows_controller import (
    update_rows_controller,
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
        "get-column-configurations",
        get_dataset_columns_controller,
        name="get_dataset_columns",
    ),
    path("get-rows", get_dataset_rows_controller, name="get_dataset_rows"),
    path("update-columns", update_columns_controller, name="update_columns"),
    path("update-rows", update_rows_controller, name="update_rows"),
    path("get-data-types", get_data_types_controller, name="get_data_types"),
    path("get-data-roles", get_data_roles_controller, name="get_data_roles"),
    path("get-merge-preview", get_merge_preview_controller, name="get_merge_preview"),
    path("merge-datasets", merge_datasets_controller, name="merge_datasets"),
]
