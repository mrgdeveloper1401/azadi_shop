from rest_framework.exceptions import APIException


class ErrorResponse(APIException):
    status_code = 400

    def __init__(self, message: str,):
        self.message = message
        super().__init__(self.message)


OBJECT_ALREADY_EXISTS = ErrorResponse("object already exists")
MAX_UPLOADING_SIZE = ErrorResponse("max uploading size")
