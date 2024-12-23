from django.urls import reverse
from django.test import  TestCase
from common.test_utils import create_logged_in_client


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
