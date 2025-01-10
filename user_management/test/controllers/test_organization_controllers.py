"""Tests for organization controllers"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from common.test_utils import (
    create_logged_in_client,
    create_test_organization,
)


# Create your tests here.


class OrganizationTestCase(TestCase):
    """OrganizationController test cases"""

    def setUp(self):
        """OrganizationControllerTestCase.setUpTestData()"""
        self.client, self.user = create_logged_in_client()
        self.org = create_test_organization()

    def test_create_organization_controller(self):
        """Test CreateOrganizationController."""
        response = self.client.post(
            reverse("create-organization"),
            {
                "name": "TestOrganization",
            },
        )

        self.assertEqual(response.data["status"], status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Organization created successfully")

    def test_get_organizations_users_by_user_id(self):
        """Test get organizations users by user id"""

        response = self.client.get(
            reverse("get-organizations-users-by-user-id", args=[self.org.id])
        )

        self.assertEqual(response.data["status"], status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Organization users retrieved successfully"
        )

    def test_get_users_from_organization_by_role_controller(self):
        """Test get users from organization by role id"""
        response = self.client.get(
            reverse(
                "get_users_from_organization_by_role_controller",
                args=[self.org.id, "FACILITATOR"],
            )
        )

        self.assertEqual(response.data["status"], status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Users from org retrieved successfully"
        )
