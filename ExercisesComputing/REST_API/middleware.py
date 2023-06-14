from django.conf import settings
from django.http import HttpResponse
import json

from .errors import ServiceUnavailableError

class ErrorHandlerMiddleware:

    CUSTOM_EXCEPTIONS = [ServiceUnavailableError]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def __prepare_res(self, exception):
        # msg = exception.to_json()
        msg = json.dumps ({"error" : "dupa error"})
        status_code =  300 #exception.STATUS_CODE

        return msg, status_code

    def __check_if_custom_exception(self, exception):
        # print("EXCEPTION: ",type(exception), exception, flush=True)
        # for exception_type in ErrorHandlerMiddleware.CUSTOM_EXCEPTIONS:
        #     if isinstance(exception, TypeError):
        #         return True
        return True

    def process_exception(self, request, exception):
        # if not settings.DEBUG:
        msg = json.dumps ({"error" : "dupa error"})
        status = 500
        if self.__check_if_custom_exception(exception) is True:
            msg, status = self.__prepare_res(exception)
            # print("****DUPA****", flush=True)

        return HttpResponse(f"{msg}", status=status)