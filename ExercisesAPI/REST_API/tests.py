from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from REST_API.models import Language, Exercise, ExerciseTest
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken





class ExerciseViewTest(APITestCase):
        URL = reverse("exercise")


        def get_token(self):
                user = AnonymousUser
                refresh = RefreshToken.for_user(user)
                return str(refresh.access_token)


        def setUp(self) -> None:
                self.language = Language.objects.create(name="Python")
                self.exercise = Exercise.objects.create(name="Palindrome", language=self.language)
                self.test1 = ExerciseTest.objects.create(exercise=self.exercise, input="kajak", output=True)
                self.test2 = ExerciseTest.objects.create(exercise=self.exercise, input="anna", output=True)
                self.test3 = ExerciseTest.objects.create(exercise=self.exercise, input="lajkonik", output=True)
                self.token = self.get_token()
        
        def test_should_return_401_no_authorization(self) -> None:
                response = self.client.get(ExerciseViewTest.URL, {"language":self.language.name, "name": self.exercise.slug })
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        def test_should_return_200_and_authorizated(self) -> None:
                print(self.token)
                response = self.client.get(ExerciseViewTest.URL, {"language":self.language.name, "name": self.exercise.slug }, Authorization=f"Bearer {self.token}")
                print(response)
                self.assertEqual(response.status_code, status.HTTP_200_OK)



