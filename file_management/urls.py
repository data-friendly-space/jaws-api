"""This module contains the urls related with analysis stuff"""

from django.urls import path

from file_management.interfaces.controllers.create_presigned_url_upload_file_controller import (
    create_presigned_url_upload_file_controller,
)

urlpatterns = [
    path(
        "get-upload-file-url",
        create_presigned_url_upload_file_controller,
        name="get_upload_file_url",
    ),
]
