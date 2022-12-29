# Tests for user api

from django.test import (
    TestCase,
)
from django.contrib.auth import (
    get_user_model,
)
from django.urls import (
    reverse,
)

from rest_framework.test import (
    APIClient,
)
from rest_framework import (
    status,
)

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(
    **params,
):
    # Create and return new user
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(
        self,
    ):
        # Test to check user creation
        payload = {
            "email": "test_user@example1.com",
            "password": "test_password",
            "name": "Test 1 name",
        }

        res = self.client.post(
            CREATE_USER_URL,
            payload,
        )

        self.assertEqual(
            res.status_code,
            status.HTTP_201_CREATED,
        )
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn(
            "password",
            res.data,
        )

    def test_user_with_email_exits_error(
        self,
    ):
        # Test error if email exits
        payload = {
            "email": "test_user@example1.com",
            "password": "test_password",
            "name": "Test 2 name",
        }

        create_user(**payload)

        res = self.client.post(
            CREATE_USER_URL,
            payload,
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_password_too_short_error(
        self,
    ):
        # Test an error if password is too short
        payload = {
            "email": "test_user@example2.com",
            "password": "pass",
            "name": "Test 3 name",
        }
        res = self.client.post(
            CREATE_USER_URL,
            payload,
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(
        self,
    ):
        """Test generates token for valid credentials."""
        user_details = {
            "name": "Test 4 name",
            "email": "test@example.com",
            "password": "test-user-password123",
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(
            TOKEN_URL,
            payload,
        )

        self.assertIn(
            "token",
            res.data,
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK,
        )

    def test_create_token_bad_credentials(
        self,
    ):
        # Checks for wrong credentials pass
        user_details = {
            "email": "test_user@exampl5.com",
            "password": "password1_for_User!",
        }

        payload = {
            "email": user_details["email"],
            "password": "baddpassword",
        }

        res = self.client.post(
            TOKEN_URL,
            payload,
        )
        self.assertNotIn(
            "token",
            res.data,
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_token_blank_password_error(
        self,
    ):
        # checkes for blank passwords
        payload = {
            "email": "test_user@exampl6.com",
            "password": "",
        }

        res = self.client.post(
            TOKEN_URL,
            payload,
        )
        self.assertNotIn(
            "token",
            res.data,
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_retrieve_user_unauthorized(self):
        # Test authentication is required for user
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    # Test private api requests with authentications
    def setUp(self):
        self.user = create_user(
            email="test_private@example.com",
            password="PasswordPrivate!",
            name="Private Test Name",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_Retrieve_profile_success(self):
        # Test retrieving profile for logged in user
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {"name": self.user.name, "email": self.user.email}
        )

    def test_post_me_not_available(self):
        # Test POST METHOD IS DESABLED OR NOT

        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        # Test to update user profile for authenticated user
        payload = {
            "name": "updated name",
            "password": "newpassword123",
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
