from cgi import test
from celery import shared_task
from .computing import CodeComputing
from rest_framework.response import Response
from django.http import JsonResponse
# from prometheus_client import Summary
from .metrics import Metrics


# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


# @shared_task()
# @REQUEST_TIME.time()
# def test_task(header_token, data):
#     computing = CodeComputing(header_token, data)
#     return computing.execute_computing()

@shared_task()
def test_task(token, data_data):
    # Metrics.upload_urls_created.collect()
    computing = CodeComputing(header_token = token, data = data_data)
    test = computing.execute_computing()
    return test
