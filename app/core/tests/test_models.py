from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "TestPassword123!"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_email = [
            ["xyz@GMAIL.com", "xyz@gmail.com"],
            ["xyz2@GMAIL.COM", "xyz2@gmail.com"],
            ["Mukund_2001@Gmail.com", "Mukund_2001@gmail.com"],
            ["MUKUND_2002@GMAIL.com", "MUKUND_2002@gmail.com"],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "123456")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            "test_superuser@example.com", "1234567890"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
