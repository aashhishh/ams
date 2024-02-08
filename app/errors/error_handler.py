import uuid
from requests import Response


def parse_error(code: str, details, description=None, exc=None) -> dict:
    request_uuid = str(uuid.uuid4())
    if isinstance(description, Response):
        description = str(description.content)

    errors = {
        'http_code': 401,
        'code': code,
        'status': False,
        'message': details,
        'exc': str(exc),
        'data':[]
    }

    return errors

def parse_alreadyExist_error(code: str, details,description=None, exc=None) -> dict:
    request_uuid = str(uuid.uuid4())
    if isinstance(description, Response):
        description = str(description.content)

    errors = {
        'http_code': 200,
        'code':code,
        'status': False,
        'message': details,
        'exc': str(exc),
        'data':[]
    }

    return errors


def parse_mongo_error(code: str, details,description=None, exc=None) -> dict:
    request_uuid = str(uuid.uuid4())

    if isinstance(exc, Exception):
        pass

    errors = {
        'code': code,
        'status': False,
        'http_code': 500,
        'message': details,
        'exc': str(exc),
        'data':[]
    }

    return errors
