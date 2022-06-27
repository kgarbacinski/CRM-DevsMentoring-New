from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from REST_API.models import Exercise, ExerciseTest, Language
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ExerciseViewTest(APITestCase):
    URL = reverse("exercise")

    def get_token(self) -> str:
        user = AnonymousUser
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @classmethod
    def setUpTestData(cls) -> None:
        cls.language = Language.objects.create(name="Python")
        cls.exercise = Exercise.objects.create(name="Palindrome", language=cls.language)
        cls.test1 = ExerciseTest.objects.create(
            exercise=cls.exercise, input="kajak", output=True
        )
        cls.test2 = ExerciseTest.objects.create(
            exercise=cls.exercise, input="anna", output=True
        )
        cls.test3 = ExerciseTest.objects.create(
            exercise=cls.exercise, input="lajkonik", output=True
        )

    def setUp(self) -> None:
        self.token = self.get_token()

    def test_should_return_401_no_authorization(self) -> None:
        response = self.client.get(
            ExerciseViewTest.URL,
            {"language": self.language.name, "name": self.exercise.slug},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_200_and_authorizated(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(
            ExerciseViewTest.URL,
            {"language": self.language.name, "name": self.exercise.slug},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_404_not_found(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(
            ExerciseViewTest.URL, {"language": "test", "name": "test"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_tests(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(
            ExerciseViewTest.URL,
            {"language": self.language.name, "name": self.exercise.slug},
        )
        expected_response = [
            OrderedDict([("input", "kajak"), ("output", "True")]),
            OrderedDict([("input", "anna"), ("output", "True")]),
            OrderedDict([("input", "lajkonik"), ("output", "True")]),
        ]
        self.assertEqual(response.data, expected_response)
