from cgi import test
from celery import shared_task
from .computing import CodeComputing
from rest_framework.response import Response
from django.http import JsonResponse

@shared_task()
def test_task(token, data_data):
    computing = CodeComputing(header_token = token, data = data_data)
    test = computing.execute_computing()
    print('aaaa', test)
    return test
