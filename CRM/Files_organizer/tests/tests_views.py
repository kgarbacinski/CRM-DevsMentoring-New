from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from Files_organizer.models import ProgrammingPath, Subject
from Files_organizer.views import ProgramingPathView


class ProgrammingPathViewTest(TestCase):
    URL = reverse("programming_path")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "Jan Kowalski", "kowalski@gmail.com", "kowalski"
        )

    def test_context(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(ProgrammingPathViewTest.URL)
        self.assertIn("paths", response.context)

    def test_should_redirect_not_logged_user_to_login_page(self):
        response = self.client.get(ProgrammingPathViewTest.URL)
        self.assertRedirects(response, "/?next=/files/")

    def test_call_view_load(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(self.URL, follow=True)
        self.assertTemplateUsed(response, "Files_organizer/files-start.html")


class SubjectViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.logo_image = SimpleUploadedFile(
            name="logo_image.jpg", content=b"", content_type="image/jpeg"
        )
        cls.path_image = SimpleUploadedFile(
            name="path_image.jpg", content=b"", content_type="image/jpeg"
        )
        cls.user = User.objects.create_user(
            "Jan Kowalski", "kowalski@gmail.com", "kowalski"
        )
        cls.programming_path = ProgrammingPath.objects.create(
            name="Python",
            about="Python programming language",
            logo_image=cls.logo_image,
            path_image=cls.path_image,
        )

    def test_context(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(
            reverse("subject", kwargs={"path": self.programming_path.slug})
        )
        self.assertIn("subjects", response.context)

    def test_should_redirect_not_logged_user_to_login_page(self):
        response = self.client.get(
            reverse("subject", kwargs={"path": self.programming_path.slug})
        )
        self.assertRedirects(response, f"/?next=/files/{self.programming_path.slug}/")
