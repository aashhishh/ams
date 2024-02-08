from app.auth.token_authentication import authorize_token
from app.errors.error_handler import parse_error
from app.errors.exceptions import AuthenticationException
from fastapi import Request


async def token_validation(request: Request) -> bool:
    is_valid_payload = await authorize_token(request)
    if is_valid_payload:
        return True

    errors = parse_error('ZA001', 'Authentication Error')
    raise AuthenticationException(status_code=401, detail=errors)
