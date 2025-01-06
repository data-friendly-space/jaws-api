import uuid

from django.test import TestCase

from common.test_utils import create_logged_in_client
from interaction_notification_mngr.service.impl.notification_service_impl import NotificationServiceImpl


class TestNotificationService(TestCase):

    def setUp(self):
        self.client, self.user = create_logged_in_client()
        self.service = NotificationServiceImpl()

    def test_get_user_notifications(self):
        notifications = self.service.get_user_notifications(None, user_id=uuid.uuid4())
        self.assertEqual(len(notifications), 0)
