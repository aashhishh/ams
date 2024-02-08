from fastapi.exceptions import HTTPException


class AuthenticationException(HTTPException):
    def __init__(self, status_code: int, detail, name='AuthenticationException'):
        super().__init__(status_code=status_code, detail=detail)
        self.name = name


class RequestException(HTTPException):
    def __init__(self, status_code: int, detail, name='RequestException'):
        super().__init__(status_code=status_code, detail=detail)
        self.name = name
