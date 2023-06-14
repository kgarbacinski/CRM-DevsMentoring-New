import json
class ServiceUnavailableError(Exception):
    def __init__(self, message):
        super().__init__(message)

    # def error_message(self):
    #     return json.dumps(self.message)


    STATUS_CODE = 503

    # def __str__(self):
    #     return "Internal service unavailable!"

    # def __repr__(self) -> str:
    #     return self.to_json()

    # def to_json(self):
    #     return json.dumps({"error": "Internal service unavailable!"})