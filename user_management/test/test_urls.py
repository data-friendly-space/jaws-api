from django.test import SimpleTestCase
from django.urls import reverse, resolve

from user_management.interfaces.controllers.create_user_controller import create_user_controller
from user_management.interfaces.controllers.get_users_controller import get_users_controller
from user_management.interfaces.controllers.refresh_token_controller import refresh_token_controller
from user_management.interfaces.controllers.sign_in_controller import sign_in_controller
from user_management.interfaces.controllers.sign_up_controller import sign_up_controller
from user_management.interfaces.controllers.verify_token_controller import verify_token_controller


class TestUrls(SimpleTestCase):

    def test_get_users_url_resolves(self):
        url = reverse("get_users")
        self.assertEqual(resolve(url).func, get_users_controller)

    #    def test_create_user_url_resolves(self):
    #       url = reverse("create_user")
    #      self.assertEqual(resolve(url).func, create_user_controller)

    def test_sign_up_url_resolves(self):
        url = reverse("sign_up")
        self.assertEqual(resolve(url).func, sign_up_controller)

    def test_sign_in_url_resolves(self):
        url = reverse("sign_in")
        self.assertEqual(resolve(url).func, sign_in_controller)

    def test_token_refresh_resolves(self):
        url = reverse("token_refresh")
        self.assertEqual(resolve(url).func, refresh_token_controller)

    def test_session_verify_resolves(self):
        url = reverse("session_verify")
        self.assertEqual(resolve(url).func, verify_token_controller)
