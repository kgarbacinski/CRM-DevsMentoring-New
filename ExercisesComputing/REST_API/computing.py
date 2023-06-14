import os
from re import A
import secrets
import subprocess
from abc import ABC, abstractmethod
from asyncio.subprocess import STDOUT
from typing import Dict, List
from .errors import ServiceUnavailableError

import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


class Handler(ABC):
    def __init__(self, user_code: Dict, code_tests: List, file_extension, terminal_command) -> None:
        self.code_tests = code_tests
        self.user_code = user_code
        self.passed_test = 0
        self.test_results = []
        self.terminal_comand = terminal_command
        self.file_extension = file_extension

    def create_file(self, test_input):
        unique_name = secrets.token_hex(nbytes=16)
        path = f"{os.getcwd()}/files/{unique_name}{self.file_extension}"
        with open(path, "w") as file:
            file.write(self.exec_code(test_input))
        return file

    def check_results(self, file, test_output):
        # print("TEST_OUTPUT ", test_output)
        try:
            result = (
                subprocess.check_output(
                    [self.terminal_comand, file.name], stderr=STDOUT
                )
                .strip()
                .decode("utf-8")
            )
        except subprocess.CalledProcessError as e:
            return self.handle_error(e)
        else:
            # TODO add test output to test_results
            if result == test_output:
                self.passed_test += 1
                self.test_results.append({"test_passed": True})
            else:
                self.test_results.append({"test_passed": False})
        finally:
            os.remove(file.name)

    def execute_computing(self):
        for test_number in range(len(self.code_tests)):
            self.file = self.create_file(self.code_tests[test_number].get("input"))
            self.test = self.check_results(self.file, self.code_tests[test_number].get("output"))
        return self.get_response(self.test)

    def get_response(self, test):
        if self.passed_test == len(self.code_tests):
            return {"is_all_tests_passed": True, "status": status.HTTP_200_OK}
        return {
            "is_all_tests_passed": False,
            "quntity_of_passed_tests": f"{self.passed_test}/{len(self.code_tests)}",
            "distinct_tests_results": self.test_results,
            "error_message": test,
        }

    @abstractmethod
    def handle_error(self, e):
        raise NotImplementedError

    @abstractmethod
    def exec_code(self, *args):
        raise NotImplementedError


class PythonHandler(Handler):
    def __init__(self, user_code, code_tests):
        super().__init__(user_code, code_tests, file_extension=".py", terminal_command="python3")

    def exec_code(self, test_input):
        return f"{self.user_code.get('code')}\nprint({self.user_code.get('name')}({test_input}))"

    def handle_error(self, e):
        error_list = e.output.strip().decode("utf-8").split("\n")
        return {"error_message": error_list[-1]}


class JavaHandler(Handler):
    def __init__(self, user_code, code_tests):
        super().__init__(user_code, code_tests, file_extension=".java", terminal_command="java")

    def exec_code(self, test_input):
        return f"class Main{{{self.user_code.get('code')} public static void main(String[] args) {{System.out.println({self.user_code.get('name')}({test_input}));}}}}"

    def handle_error(self, e):
        error_list = e.output.strip().decode("utf-8").split("\n")
        error_message = error_list
        return {"error_message": error_message}


class JavaScriptHandler(Handler):
    def __init__(self, user_code, code_tests):
        super().__init__(user_code, code_tests, file_extension=".js", terminal_command="node")

    def exec_code(self, test_input):
        return f"{self.user_code.get('code')} console.log({self.user_code.get('name')}({test_input}))"

    def handle_error(self, e):
        error = e.output.strip().decode("utf-8").split("\n")
        return {"error": error[4]}


class CodeComputing:
    HANDLERS = {
        "Python": PythonHandler,
        "Java": JavaHandler,
        "JavaScript": JavaScriptHandler,
    }

    def __init__(self, header_token: str, user_code: Dict):
        self.user_code = user_code
        self.header_token = header_token
        self.code_tests = self.get_code_tests()
        self.handler = CodeComputing.HANDLERS.get(self.user_code.get("language", "Python"), PythonHandler)(
            self.user_code, self.code_tests)

    def get_code_tests(self):
        try:
            code_tests = requests.get(
                settings.API_URL,
                params={
                    "name": self.user_code.get("name"),
                    "language": self.user_code.get("language"),
                },
                headers={"Authorization": self.header_token},
            ).json()
        except Exception:
            # print("Computing error ", e, flush=True)
            # return {"error_message": ServiceUnavailableError}
            message = {"error_message": "no connection"}
            raise ServiceUnavailableError(message=message)
        else:
            return code_tests
        # return self.code_tests

    def execute_computing(self):
        return self.handler.execute_computing()
