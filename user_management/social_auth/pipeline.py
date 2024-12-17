"""Custom pipeline for redirecting the user with JWT"""
from datetime import datetime, timedelta, UTC
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import jwt
from django.http import HttpResponseRedirect
from app import settings


def redirect_to_next_with_token(backend, user, response, *args, **kwargs):
    """Redirect the user with a JWT"""
    # Extract the 'next' parameter from the session
    next_url = "http://localhost:3000/workspaces"
    # next_url = backend.get_redirect_uri('next')

    # Get the access token from the response
    access_token = response.get('access_token')

    if not access_token or not next_url:
        return  # If no access token is found or no next URL is found, do nothing

    # Create a signed JWT token
    payload = {
        'access_token': access_token,
        'user_id': str(user.id),
        'exp': datetime.now(UTC) + timedelta(hours=24)
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    # Parse the next URL and add the access token as a query parameter
    url_parts = list(urlparse(next_url))
    query = dict(parse_qs(url_parts[4]))  # Get existing query parameters
    query['token'] = jwt_token  # Add the access token
    url_parts[4] = urlencode(query)  # Re-encode query string

    # Rebuild the URL with the access token
    redirect_url = urlunparse(url_parts)

    # Redirect to the next URL with the access token
    return HttpResponseRedirect(redirect_url)
