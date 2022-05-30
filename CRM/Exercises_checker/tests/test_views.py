
from django.test import TestCase
from django.test import TestCase, RequestFactory
from django.urls import reverse
from Exercises_checker.views import TasksListView, TaskDetailView
from Exercises_checker.models import Exercise, Language, ExerciseStatus
from django.contrib.auth.models import User
from rest_framework import status


class TasksListViewTest(TestCase):
    URL = reverse("exercises-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('Jan Kowalski', 'kowalski@gmail.com', 'kowalski')

    def test_context(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(TasksListViewTest.URL)
        self.assertIn('languages', response.context)

    def test_should_redirect_not_logged_user_to_login_page(self):
        response = self.client.get(TasksListViewTest.URL)
        self.assertRedirects(response, '/?next=/exercises/')

    def test_call_view_load(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(self.URL, follow=True)
        self.assertTemplateUsed(response, 'Exercises_checker/exercises-list.html')



class TaskDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('Jan Kowalski', 'kowalski@gmail.com', 'kowalski')
        cls.language = Language.objects.create(name="Python")
        cls.exercise = Exercise.objects.create(name="Palindrome", language=cls.language, description="Write Palindrome", type="EASY")
        cls.language.user.add(cls.user)
        cls.language.save()
        cls.exercise_status = ExerciseStatus.objects.get(user=cls.user, exercise=cls.exercise)        

    def test_context(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(reverse('exercise',kwargs={'pk':self.exercise.id}))
        self.assertIsInstance(response.context['exercise_status'], ExerciseStatus)

    def test_should_redirect_not_logged_user_to_login_page(self):
        response = self.client.get(reverse("exercise", kwargs={'pk':5}), follow=True)
        self.assertRedirects(response, '/?next=/exercises/5/')

    def test_should_return_404_exercise_status_not_found(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(reverse("exercise", kwargs={'pk':5}), follow=True)
        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_call_view_load(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(reverse("exercise", kwargs={'pk':self.language.id}))
        self.assertTemplateUsed(response, 'Exercises_checker/exercise.html')



    