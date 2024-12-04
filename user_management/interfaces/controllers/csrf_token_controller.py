from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators import http
from rest_framework.decorators import api_view


@http.require_safe
@api_view(['GET'])
def csrf_token_controller(request):
    response = JsonResponse({"success": True})
    response.set_cookie('csrftoken', get_token(request))
    return response
