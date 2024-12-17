from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from analysis.models.analysis import Analysis
from common.test_utils import create_logged_in_client
from user_management.models import Organization, Role, Workspace
from user_management.models.user_organization_role import UserOrganizationRole


# Create your tests here.


class OrganizationTestCase(TestCase):
    """OrganizationController test cases"""

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        """OrganizationControllerTestCase.setUpTestData()"""
        self.client, self.user = create_logged_in_client()
        self.mockUser = {
            "name": "TestName1",
            "lastname": "TestLastname1",
            "email": "test1@test.com",
            "password": "testpassword1"
        }
        self.org = Organization.objects.create(name="TestOrganization1")
        self.workspace = Workspace.objects.create(title="TestWorkspace1", organization=self.org,
                                                  facilitator_id=self.user.id, creator_id=self.user.id)
        self.role = Role.objects.get_or_create(role="FACILITATOR")
        self.analysis = Analysis.objects.create(title="TestAnalysis1", workspace_id=self.workspace.id,
                                                end_date='2024-12-17', creator_id=self.user.id)
        UserOrganizationRole.objects.create(user=self.user, organization_id=self.org.id, role_id=self.role[0].id)

    def test_create_organization_controller(self):
        """Test CreateOrganizationController."""
        response = self.client.post(reverse('create-organization'), {
            "name": "TestOrganization",
        })

        self.assertEqual(response.data['status'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Organization created successfully')

    def test_get_organizations_users_by_user_id(self):
        """Test get organizations users by user id"""
        response = self.client.get(reverse('get-organizations-users-by-user-id'))

        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Organization users retrieved successfully')

    def test_get_users_from_organization_by_role_controller(self):
        """Test get users from organization by role id"""
        response = self.client.get(
            reverse('get_users_from_organization_by_role_controller', args=[self.org.id, "FACILITATOR"]))

        self.assertEqual(response.data['status'], status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Users from org retrieved successfully')
