import os
import secrets
import subprocess
from abc import ABC, abstractmethod
from asyncio.subprocess import STDOUT
from typing import Dict, List
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.http import JsonResponse


class Handler(ABC):
    def __init__(self, data: Dict, tests: List, extension, terminal_command) -> None:
        self.tests = tests
        self.data = data
        self.passed_test = 0
        self.terminal_comand = terminal_command
        self.extension = extension

    def create_file(self, test_input):
        print('DUPA 3')
        unique_name = secrets.token_hex(nbytes=16)
        path = (f'{os.getcwd()}/files/{unique_name}{self.extension}')
        with open(path, "w+") as file:
            file.write(self.exec_code(test_input))
        return file

    def check_results(self, file, test_output):

        try:
            result = subprocess.check_output([self.terminal_comand, file.name], stderr=STDOUT).strip().decode('utf-8')

        except subprocess.CalledProcessError as e:
            self.handle_error(e)

        finally:
            os.remove(file.name)

        if result == test_output:
            self.passed_test += 1

    def handle_error(self, e):
        error = e.output.strip().decode('utf-8').split('\n')
        error = "".join(error[1:])
        # return Response({"error": error})
        raise ValidationError({"error": error})

    def execute_computing(self):
        for test in self.tests:
            file = self.create_file(test.get('input'))
            self.check_results(file, test.get('output'))
        return self.get_response()

    def get_response(self):
        if self.passed_test == len(self.tests):
            # return Response({"done":True}, status=status.HTTP_200_OK)
            return {'done': True}
        # return Response({"done":False, "test_passed": f"{self.passed_test}/{len(self.tests)}"}, status=status.HTTP_200_OK)
        return {"done": False, "test_passed": f"{self.passed_test}/{len(self.tests)}"}

    @abstractmethod
    def exec_code(self):
        raise NotImplementedError


class PythonHandler(Handler):

    def __init__(self, data, tests):
        super().__init__(data, tests, extension=".py", terminal_command="python3")

    def exec_code(self, test_input):
        return f"{self.data.get('code')}\nprint({self.data.get('name')}({test_input}))"


class JavaHandler(Handler):
    def __init__(self, data, tests):
        super().__init__(data, tests, extension=".java", terminal_command="java")

    def exec_code(self, test_input):
        return f"class Main{{{self.data.get('code')} public static void main(String[] args) {{System.out.println({self.data.get('name')}({test_input}));}}}}"


class JavaScriptHandler(Handler):
    def __init__(self, data, tests):
        super().__init__(data, tests, extension=".js", terminal_command="node")

    def exec_code(self, test_input):
        return f"{self.data.get('code')} console.log({self.data.get('name')}({test_input}))"

    def handle_error(self, e):
        error = e.output.strip().decode('utf-8').split('\n')
        error = "".join(error[6:])
        raise ValidationError({"error": error})


class CodeComputing:
    HANDLERS = {"Python": PythonHandler, "Java": JavaHandler, "JavaScript": JavaScriptHandler}

    def __init__(self, header_token: str, data: Dict):
        self.data = data
        self.header_token = header_token
        self.tests = self.get_tests()
        self.handler = CodeComputing.HANDLERS.get(self.data.get("language"))(self.data, self.tests)

    def get_tests(self):
        tests = requests.get(settings.API_URL,
                             params={"name": self.data.get('name'), "language": self.data.get("language")},
                             headers={"Authorization": self.header_token}).json()
        return tests

    def execute_computing(self):
        return self.handler.execute_computing()
