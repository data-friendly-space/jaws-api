from django.test import TestCase

from analysis.models.analysis import Analysis
from common.exceptions.exceptions import NotFoundException, BadRequestException
from common.test_utils import create_logged_in_client
from user_management.contract.io.create_organization_in import CreateOrganizationIn
from user_management.models import Organization, Workspace, Role
from user_management.models.user_organization_role import UserOrganizationRole
from user_management.service.impl.organization_service_impl import OrganizationServiceImpl


class TestOrganizationService(TestCase):

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = OrganizationServiceImpl()
        self.org = Organization.objects.create(name="TestOrganization6")
        self.workspace = Workspace.objects.create(title="TestWorkspace7", organization=self.org,
                                                  facilitator_id=self.user.id, creator_id=self.user.id)
        self.role = Role.objects.get_or_create(role="ADMIN")
        self.analysis = Analysis.objects.create(title="TestAnalysis1", workspace_id=self.workspace.id,
                                                end_date='2024-12-17', creator_id=self.user.id)
        UserOrganizationRole.objects.create(user_id=self.user.id, role_id=self.role[0].id, organization_id=self.org.id)
        # UserWorkspaceRole.objects.create(user_id=self.user.id, role_id=self.role[0].id, workspace_id=self.workspace.id)

    def test_get_organizations(self):
        """Test get_organizations function."""
        organizations = self.service.get_organizations()
        self.assertIsInstance(organizations, list)

    def test_create_organization(self):
        """Test create org function."""
        request = {
            "name": "testorganization1",
        }
        create_organization_in = CreateOrganizationIn(data=request)
        workspace = self.service.create_organization(create_organization_in)
        self.assertIsNotNone(workspace)

    def test_create_organization_bad_request(self):
        """Test create org function. Bad Request"""
        request = {
        }
        create_organization_in = CreateOrganizationIn(data=request)
        with self.assertRaises(BadRequestException) as context:
            self.service.create_organization(create_organization_in)
        self.assertEqual(str(context.exception), "Organization request is not valid: ")

    def test_get_organizations_by_user_id(self):
        """Test get organizations by user id function."""

        org = self.service.get_organizations_by_user_id(None, self.user.id)
        self.assertIsNotNone(org)

    def test_get_organizations_users_by_user_id(self):
        """Test get organizations users by user id function."""
        org = self.service.get_organizations_users_by_user_id(self.user.id, None)
        self.assertIsNotNone(org)

    def test_get_available_organizations_by_user_id(self):
        """Test get available organizations users by user id function."""
        org = self.service.get_available_organizations_by_user_id(self.user.id)
        self.assertIsNotNone(org)

    def test_get_organization_users_by_role(self):
        """Test get organizations users by role function."""
        org = self.service.get_organization_users_by_role(self.org.id, "FACILITATOR")
        self.assertIsNotNone(org)

    def test_get_organization_users_by_role_bad_request(self):
        """Test get organizations users by role function."""
        with self.assertRaises(BadRequestException) as context:
            self.service.get_organization_users_by_role(self.org.id, None)
        self.assertEqual(str(context.exception), "Role type must be sent")

