from celery.result import AsyncResult
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .computing import CodeComputing
from .permissions import TokenVerify
from .tasks import test_task
from ExercisesComputing.celery import app

class ExerciseView(APIView):
    permission_classes = [TokenVerify]

    def post(self, request):
        task = test_task.apply_async(
            args=(request.META.get("HTTP_AUTHORIZATION", None), request.data)
        )
        return JsonResponse({"task_id": task.id})


def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return JsonResponse(result)
