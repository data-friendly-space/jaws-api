from django.test import SimpleTestCase
from django.urls import reverse, resolve

from analysis.interfaces.controllers.get_analysis_controller import get_analysis_controller
from user_management.interfaces.controllers.create_organization_controller import create_organization_controller
from user_management.interfaces.controllers.get_organization_users_controller import \
    get_organizations_users_by_user_id_controller
from user_management.interfaces.controllers.get_user_logged_organizations_controller import \
    get_available_user_organizations
from user_management.interfaces.controllers.get_user_logged_workspaces_controller import \
    get_user_logged_workspaces_controller
from user_management.interfaces.controllers.get_users_controller import get_users_controller
from user_management.interfaces.controllers.get_users_from_organization_by_role_controller import \
    get_users_from_organization_by_role_controller
from user_management.interfaces.controllers.refresh_token_controller import refresh_token_controller
from user_management.interfaces.controllers.sign_in_controller import sign_in_controller
from user_management.interfaces.controllers.sign_up_controller import sign_up_controller
from user_management.interfaces.controllers.verify_token_controller import verify_token_controller


class TestUrls(SimpleTestCase):

    def test_get_users_url_resolves(self):
        """Test get user url"""
        url = reverse("get_users")
        self.assertEqual(resolve(url).func, get_users_controller)

    #    def test_create_user_url_resolves(self):
    #       url = reverse("create_user")
    #      self.assertEqual(resolve(url).func, create_user_controller)

    def test_sign_up_url_resolves(self):
        """Test sign up url"""
        url = reverse("sign_up")
        self.assertEqual(resolve(url).func, sign_up_controller)

    def test_sign_in_url_resolves(self):
        """Test sign in url"""
        url = reverse("sign_in")
        self.assertEqual(resolve(url).func, sign_in_controller)

    def test_token_refresh_resolves(self):
        """TEst token refresh url"""
        url = reverse("token_refresh")
        self.assertEqual(resolve(url).func, refresh_token_controller)

    def test_session_verify_resolves(self):
        """Test session verification url"""
        url = reverse("session_verify")
        self.assertEqual(resolve(url).func, verify_token_controller)

    def test_get_analyses_url_resolves(self):
        """Test that get analysis url works"""
        url = reverse("get_analysis_controller", args=['some-workspace-id'])
        self.assertEqual(resolve(url).func, get_analysis_controller)

    def test_create_organization_url_resolves(self):
        """Test that the create organization URL works"""
        url = reverse("create-organization")
        self.assertEqual(resolve(url).func, create_organization_controller)

    def test_get_organizations_users_url_resolves(self):
        """Test that the get organization users by user ID URL works"""
        url = reverse("get-organizations-users-by-user-id")
        self.assertEqual(resolve(url).func, get_organizations_users_by_user_id_controller)

    def test_get_users_from_organization_by_role_url_resolves(self):
        """Test that the get users from organization by role URL works"""
        url = reverse("get_users_from_organization_by_role_controller", args=['some-organization-id', 'some-role'])
        self.assertEqual(resolve(url).func, get_users_from_organization_by_role_controller)

    def test_get_user_logged_workspaces_url_resolves(self):
        """Test that the get user logged workspaces URL works"""
        url = reverse("get_user_logged_workspaces_controller")
        self.assertEqual(resolve(url).func, get_user_logged_workspaces_controller)

    def test_get_available_user_organizations_url_resolves(self):
        """Test that the get available user organizations URL works"""
        url = reverse("get_available_organizations_by_user_id")
        self.assertEqual(resolve(url).func, get_available_user_organizations)
