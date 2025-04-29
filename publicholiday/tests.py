from django.test import TestCase
from .models import Notification
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class NotificationModelTest(TestCase):
    def setUp(self):
        self.notification = Notification.objects.create(
            title="Notification",
            message="we are testing our Notification.",
            type="info",
        )

    def test_notificatn_creation(self):
        notification = Notification.objects.get(id=self.notification.id)
        self.assertEqual(notification.title, "Notification")
        self.assertEqual(notification.message, "we are testing our Notification.")
        self.assertEqual(notification.type, "info")
        self.assertIsNotNone(notification.created_at)

    def test_notification_string_representation(self):
        self.assertEqual(str(self.notification), "Notification")

    def test_notification_type_choices(self):
        valid_types = [
            choice[0] for choice in Notification._meta.get_field("type").choices
        ]
        self.assertIn("info", valid_types)
        self.assertIn("warn", valid_types)
        self.assertIn("error", valid_types)
        self.assertIn("success", valid_types)

    def test_notification_creation_missing_title(self):
        with self.assertRaises(IntegrityError):
            Notification.objects.create(
                title=None, message="This notification has no title.", type="error"
            )

    def test_invalid_type_choice(self):
        notification = Notification(
            title="Invalid Type Notification",
            message="This has an invalid type.",
            type="invalid",
        )
        with self.assertRaises(ValidationError):
            notification.full_clean()

    def test_long_title(self):
        long_title = "x" * 300
        notification = Notification(
            title=long_title, message="Welcome back to our home.", type="info"
        )
        with self.assertRaises(ValidationError):
            notification.full_clean()

    def test_notification_creation_missing_message(self):
        with self.assertRaises(IntegrityError):
            Notification.objects.create(
                title="No Message Notification", message=None, type="warn"
            )
