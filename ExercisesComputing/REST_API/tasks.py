from celery import shared_task
from django.http import JsonResponse
from rest_framework.response import Response

from .computing import CodeComputing


@shared_task()
def test_task(token, data_data):
    computing = CodeComputing(header_token=token, data=data_data)
    test = computing.execute_computing()
    print("aaaa", test)
    return test
