# Test for recipe api

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse("recipe:recipe-list")


def create_recipe(user, **params):
    # Create and return sample recipe

    defaults = {
        "title": "Sample Recipe Title",
        "time_minutes": 5,
        "price": Decimal("5.25"),
        "description": "Sample Description",
        "link": "http://www.example.com/recipe.pdf",
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PubllicRecipeAPITests(TestCase):
    # Test to check un authenticated requests

    def setUp(self):
        self.client = APIClient

    def test_auth_required(self):
        # Test authentication is required

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    # Test authenticeated api test

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test_auth@example.com", "test_auth_password"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        # Test to retrieve list of recipe
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")

        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_limited_to_user(self):
        # Test is only to check if it is to authenticated user

        other_user = get_user_model().objects.create_user(
            "auth_other@example.com",
            "password_auth_other",
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
