from unittest.mock import patch

from django.test import TestCase

from analysis.models.analysis import Analysis
from common.exceptions.exceptions import NotFoundException, BadRequestException
from common.test_utils import create_logged_in_client
from user_management.contract.io.create_workspace_in import CreateWorkspaceIn
from user_management.models import Organization, Workspace, Role, UserWorkspaceRole
from user_management.service.impl.workspace_service_impl import WorkspaceServiceImpl


class TestWorkspaceService(TestCase):

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = WorkspaceServiceImpl()
        self.org = Organization.objects.create(name="TestOrganization1")
        self.workspace = Workspace.objects.create(title="TestWorkspace1", organization=self.org,
                                                  facilitator_id=self.user.id, creator_id=self.user.id)
        self.role = Role.objects.get_or_create(role="ADMIN")
        self.analysis = Analysis.objects.create(title="TestAnalysis1", workspace_id=self.workspace.id,
                                                end_date='2024-12-17', creator_id=self.user.id)

    def test_get_workspaces(self):
        """Test get_workspaces function."""
        workspaces = self.service.get_workspaces()
        self.assertIsInstance(workspaces, list)

    @patch('user_management.repository.workspace_repository_impl.WorkspaceRepositoryImpl.get_all')
    def test_get_workspaces_not_found(self, mock_get_workspaces):
        """Test get_workspaces function."""
        mock_get_workspaces.return_value = None
        with self.assertRaises(NotFoundException) as context:
            self.service.get_workspaces()
        self.assertEqual(str(context.exception), "Workspaces not found")

    def test_create_workspace(self):
        """Test get_workspaces function."""
        request = {
            "title": "TestWorkspace13",
            "facilitator_email": str(self.user.email),
            "organization_id": str(self.org.id),
        }
        create_workspace_in = CreateWorkspaceIn(data=request)
        workspace = self.service.create_workspace(create_workspace_in, str(self.user.id))
        self.assertIsNotNone(workspace)

    def test_create_workspace_facilitator_not_found(self):
        """Test get_workspaces function for facilitator not found."""
        request = {
            "title": "TestWorkspace13",
            "facilitator_email": "tesrads@email.com",
            "organization_id": self.org.id,
        }
        create_workspace_in = CreateWorkspaceIn(data=request)
        with self.assertRaises(NotFoundException) as context:
            self.service.create_workspace(create_workspace_in, str(self.user.id))
        self.assertEqual(str(context.exception), "Facilitator not found")

    def test_create_workspace_bad_request(self):
        """Test create workspace function bad requesst"""
        request = {
            "title": "TestWorkspace13",
        }
        create_workspace_in = CreateWorkspaceIn(data=request)
        with self.assertRaises(BadRequestException) as context:
            self.service.create_workspace(create_workspace_in, str(self.user.id))
        self.assertEqual(str(context.exception), 'Workspace request is not valid: ')

    def test_get_workspaces_by_user_id(self):
        """Test get_workspaces_by_user_id function."""
        UserWorkspaceRole.objects.create(user_id=self.user.id, role_id=self.role[0].id, workspace_id=self.workspace.id)
        workspace = self.service.get_workspaces_by_user_id(self.user.id, None)
        self.assertIsNotNone(workspace)

    def test_get_workspaces_by_user_id_not_found(self):
        """Test get_workspaces_by_user_id function not found."""
        with self.assertRaises(NotFoundException) as context:
            self.service.get_workspaces_by_user_id(self.user.id, None)
        self.assertEqual(str(context.exception), "Workspaces not found")

