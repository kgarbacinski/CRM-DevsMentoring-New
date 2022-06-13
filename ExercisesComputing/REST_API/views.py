from rest_framework.views import APIView
from .computing import CodeComputing
from .permissions import TokenVerify
from .tasks import test_task
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from django.http import JsonResponse


class ExerciseView(APIView):
    permission_classes = [TokenVerify]

    def post(self, *args, **kwargs):   
        task = test_task.apply_async(args=(self.request.META.get('HTTP_AUTHORIZATION', None), self.request.data))
        return JsonResponse({"task_id": task.id})
    


def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result)


