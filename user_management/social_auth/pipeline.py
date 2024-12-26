"""Custom pipeline for redirecting the user with JWT"""
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import AccessToken

from common.exceptions.exceptions import UnauthorizedException


def redirect_to_next_with_token(backend, user, response, *args, **kwargs):
    """Redirect the user with a JWT"""
    # Extract the 'next' parameter from the session
    next_url = backend.strategy.session_get('next')

    # Get the access token from the response
    access_token = response.get("access_token")

    if not access_token or not next_url:
        raise UnauthorizedException(
            "Something went wrong during the authentication. Please sign in again"
        )

    jwt_token = AccessToken.for_user(user)


    # Parse the next URL and add the access token as a query parameter
    url_parts = list(urlparse(next_url))
    query = dict(parse_qs(url_parts[4]))  # Get existing query parameters
    query["access"] = jwt_token  # Add the access token
    url_parts[4] = urlencode(query)  # Re-encode query string

    # Rebuild the URL with the access token
    redirect_url = urlunparse(url_parts)

    # Redirect to the next URL with the access token
    return HttpResponseRedirect(redirect_url)
