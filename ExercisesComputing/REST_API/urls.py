from django.urls import path

from .views import ExerciseView, get_status

urlpatterns = [
    path("", ExerciseView.as_view()),
    path("tasks/<task_id>/", get_status, name="get_status"),
]
