from collections import OrderedDict

from django.contrib.auth.models import User
from Exercises_checker.models import Exercise, ExerciseStatus, Language
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class ExerciseViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = User.objects.create_user(
            "Jan Kowalski", "kowalski@gmail.com", "kowalski"
        )
        cls.user2 = User.objects.create_user("Jan Nowak", "nowak@gmail.com", "nowak")
        cls.language = Language.objects.create(name="Python")
        cls.easy_exercise = Exercise.objects.create(
            name="Palindrome",
            language=cls.language,
            description="Write Palindrome",
            type="EASY",
        )
        cls.medium_exercise = Exercise.objects.create(
            name="Decorators",
            language=cls.language,
            description="Write Decorator",
            type="MEDIUM",
        )
        cls.hard_exercise = Exercise.objects.create(
            name="Fibonacci",
            language=cls.language,
            description="Write Fibonacci function",
            type="HARD",
        )
        cls.language.user.add(cls.user1)
        cls.language.save()

    def test_should_return_401_not_authenticated(self) -> None:
        response = self.client.get(
            reverse("exercise_access", kwargs={"pk": self.language.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_404_language_not_found(self) -> None:
        self.client.force_login(self.user1, backend=None)
        response = self.client.get(reverse("exercise_access", kwargs={"pk": 5}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_empty_lists_for_user_without_access(self) -> None:
        self.client.force_login(self.user2, backend=None)
        response = self.client.get(
            reverse("exercise_access", kwargs={"pk": self.language.id})
        )
        excepted_response = {
            "quantity": {
                "all_exercises_quantity": 0,
                "done_exercises_quantity": 0,
                "easy_exercises_quantity": 0,
                "done_easy_exercises_quantity": 0,
                "medium_exercises_quantity": 0,
                "done_medium_exercises_quantity": 0,
                "hard_exercises_quantity": 0,
                "done_hard_exercises_quantity": 0,
            },
            "exercises": {"easy": [], "medium": [], "hard": []},
        }
        self.assertEqual(response.data, excepted_response)

    def test_should_return_200(self) -> None:
        self.client.force_login(self.user1, backend=None)
        response = self.client.get(
            reverse("exercise_access", kwargs={"pk": self.language.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_exercises_list(self) -> None:
        self.client.force_login(self.user1, backend=None)
        response = self.client.get(
            reverse("exercise_access", kwargs={"pk": self.language.id})
        )
        excepted_response = {
            "quantity": {
                "all_exercises_quantity": 3,
                "done_exercises_quantity": 0,
                "easy_exercises_quantity": 1,
                "done_easy_exercises_quantity": 0,
                "medium_exercises_quantity": 1,
                "done_medium_exercises_quantity": 0,
                "hard_exercises_quantity": 1,
                "done_hard_exercises_quantity": 0,
            },
            "exercises": {
                "easy": [
                    OrderedDict(
                        [
                            ("done", False),
                            ("id", 1),
                            ("name", "Palindrome"),
                            ("slug", "palindrome"),
                        ]
                    )
                ],
                "medium": [
                    OrderedDict(
                        [
                            ("done", False),
                            ("id", 2),
                            ("name", "Decorators"),
                            ("slug", "decorators"),
                        ]
                    )
                ],
                "hard": [
                    OrderedDict(
                        [
                            ("done", False),
                            ("id", 3),
                            ("name", "Fibonacci"),
                            ("slug", "fibonacci"),
                        ]
                    )
                ],
            },
        }
        self.assertEqual(response.data, excepted_response)
