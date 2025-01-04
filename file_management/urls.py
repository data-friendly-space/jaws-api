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
from file_management.interfaces.controllers.testeando import testeando

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
        "testeando",
        testeando,
        name="testeando"
    )
]
