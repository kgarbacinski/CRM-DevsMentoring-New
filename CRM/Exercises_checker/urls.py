from django.urls import path, include

from .views import TasksListView, TaskDetailView

urlpatterns = [
    path("", TasksListView.as_view(), name="exercises-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="exercise"),
    path('api/', include('Exercises_checker.api.urls')),
]
