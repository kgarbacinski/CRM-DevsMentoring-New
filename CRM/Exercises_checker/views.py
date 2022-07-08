from re import S

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Exercise, ExerciseStatus, Language


class TasksListView(LoginRequiredMixin, ListView):
    template_name = "Exercises_checker/exercises-list.html"
    model = Language
    context_object_name = "languages"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = ExerciseStatus
    context_object_name = "exercise_status"
    template_name = "Exercises_checker/exercise.html"

    def get_object(self, queryset=None):
        exercise_status = (
            ExerciseStatus.objects.filter(user=self.request.user)
            .filter(exercise__id=self.kwargs["pk"])
            .first()
        )
        if not exercise_status:
            raise Http404
        return exercise_status
