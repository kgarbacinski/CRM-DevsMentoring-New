from celery import shared_task
from ExercisesComputing.celery import app
from celery.exceptions import Ignore
import json

from celery.result import AsyncResult
from django.http import JsonResponse

# from prometheus_client import Summary
from .metrics import Metrics
from .computing import CodeComputing


# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


# @shared_task()
# @REQUEST_TIME.time()
# def test_task(header_token, data):
#     computing = CodeComputing(header_token, data)
#     return computing.execute_computing()


@shared_task(bind=True, max_retries=1)
def test_task(self, token, data_data):
    # computing = CodeComputing(header_token=token, user_code=data_data)
    # test = computing.execute_computing()
    # return test
    # return {"error_message": "task_error"}
    try:
        computing = CodeComputing(header_token=token, user_code=data_data)
    except Exception as err:
        print("ERROR from computing:", json.dumps(err))
        dupa = json.dumps(err)
        print("message form connection: ", dupa)
        # return {err}
        return {"error_message": "sss"}
    else:
        test = computing.execute_computing()
        return test
    # Metrics.upload_urls_created.collect()
    # task_id = self.AsyncResult(self.request.id).state
    # computing = CodeComputing(header_token=token, user_code=data_data)

    # try:
    #     # task_id = self.AsyncResult(self.request.id).state
    #     # print("TASK STATUS: ", self.AsyncResult(self.request.id).state)
    #     computing = CodeComputing(header_token=token, user_code=data_data)
    #     # print("COMPUTING task: ", computing)
    #     test = computing.execute_computing()
    #     return test
    # except Exception as e:
    #     # print("Task error ", e, flush=True)
    #     return {"error_message": "task_error"}
    #     # return self.state.FAILURE
    #     # app.control.revoke(task_id, terminate=True)
    #     # raise Ignore()

    # print("COMPUTING: ",computing.__dict__)

