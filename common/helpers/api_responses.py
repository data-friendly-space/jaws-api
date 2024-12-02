from rest_framework.response import Response
from rest_framework import status, serializers


class APIResponseSuccess(serializers.Serializer):
    status = serializers.CharField(default='success', allow_null=True)
    message = serializers.CharField(default='', allow_null=True)
    data = serializers.DictField(default={}, allow_null=True)


class APIResponseError(serializers.Serializer):
    status = serializers.CharField(default='error', allow_null=True)
    message = serializers.CharField(default='', allow_null=True)
    errors = serializers.DictField(default={}, allow_null=True)


def api_response_success(message="Success", data=None, status_code=status.HTTP_200_OK):
    response_data = {
        'message': message,
        'payload': data,
        'status': status_code
    }

    serializer = APIResponseSuccess(data=response_data)
    return Response(serializer.initial_data, status=status_code)


def api_response_error(message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    response_data = {
        'message': message,
        'errors': errors,
        'status': status_code
    }

    serializer = APIResponseError(data=response_data)
    return Response(serializer.initial_data, status=status_code)
