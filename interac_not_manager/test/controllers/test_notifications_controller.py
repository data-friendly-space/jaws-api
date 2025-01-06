from django.urls import reverse
from django.test import TestCase
from common.test_utils import create_logged_in_client
from interac_not_manager.models.notification import Notification
from interac_not_manager.service.utils.messages import ORGANIZATION_INVITE_MESSAGE


class GetNotificationsControllerTests(TestCase):
    """Get notifications controller tests"""

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.url = reverse("get_user_notifications_controller")

    def test_get_user_notifications(self):
        """Test get user notifications"""
        response = self.client.get(self.url)
        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['message'], 'User notifications retrieve successfully')


class DeleteNotificationByIdControllerTests(TestCase):
    def setUp(self):
        self.client, self.user = create_logged_in_client()
        notification = Notification.objects.create(user=self.user, message=ORGANIZATION_INVITE_MESSAGE, type="Info")
        self.url = reverse("delete_notification_by_id_controller",args=[notification.id])

    def test_delete_notification(self):
        """Test get user notifications"""
        response = self.client.delete(self.url)
        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['message'], 'Notification deleted successfully')
