from fastapi import Response
from fastapi import HTTPException




class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, existing_contact: list):
        super().__init__(status_code=status_code, detail=detail)
        self.existing_contact = existing_contact





class BadRequest(Response):
    def __init__(self, content=''):
        super().__init__(status_code=400, content=content)


class NotFound(Response):
    def __init__(self, content=''):
        super().__init__(status_code=404, content=content)


class Unauthorized(Response):
    def __init__(self, content=''):
        super().__init__(status_code=401, content=content)


class NoContent(Response):
    def __init__(self):
        super().__init__(status_code=204)


class MessageServiceError(Exception):
    pass