from rest_framework import status
from rest_framework.decorators import api_view

from user_management.interfaces.controllers.helpers import api_response


@api_view(['GET'])
def get_users_controller(request):

    return api_response("User retrieved", [], status.HTTP_200_OK)
