from rest_framework import status
from rest_framework.response import Response


def api_response(message="Success", data=None, status_code=status.HTTP_200_OK):
    response_data = {
        'message': message,
        'payload': data,
        'status': status_code
    }

    return Response(response_data, status=status_code)


