from django.test import TestCase
from Exercises_checker.models import Exercise, Language, ExerciseStatus
from django.contrib.auth.models import User

class ExerciseStatusM2mTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('Jan Kowalski', 'kowalski@gmail.com', 'kowalski')
        cls.language = Language.objects.create(name="Python")
        cls.exercise_1 = Exercise.objects.create(name="Palindrome", language=cls.language, description="Write Palindrome", type="EASY")
        cls.exercise_2 = Exercise.objects.create(name="Decorators", language=cls.language, description="Write Decorator", type="Medium")
        cls.language.user.add(cls.user)
        cls.language.save()

    def test_should_create_exercise_status_for_new_user_in_specified_language(self):
        exercise_status_1 = ExerciseStatus.objects.filter(exercise= self.exercise_1, user=self.user).exists()
        exercise_status_2 = ExerciseStatus.objects.filter(exercise= self.exercise_2, user=self.user).exists()
        self.assertTrue(exercise_status_1, True)
        self.assertTrue(exercise_status_2, True)





       



