from django.urls import include, path

from .views import TaskDetailView, TasksListView

urlpatterns = [
    path("", TasksListView.as_view(), name="exercises-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="exercise"),
    path("api/", include("Exercises_checker.api.urls")),
]
