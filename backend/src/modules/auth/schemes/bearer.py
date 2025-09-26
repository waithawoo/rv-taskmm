from fastapi import Request, HTTPException

from src.db.redis import TokenBlocklist
from ..exceptions import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
)
from ..utils import decode_jwt_token
from .base import Auth, HTTPAuthorizationCredentials


class BearerTokenAuth(Auth.scheme('bearer')):
    def __init__(self, auto_error=False):
        super().__init__(auto_error=auto_error)
        self.token_blocklist = TokenBlocklist()

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        if not creds:
            raise AccessTokenRequired()

        token = creds.credentials
        if not token:
            authorization: str | None = request.headers.get('Authorization')
            if not authorization or not authorization.startswith('Bearer '):
                raise HTTPException(
                    status_code=401, detail='Invalid or missing Bearer token.'
                )
            token = authorization.split('Bearer ')[1]

        if not self._token_valid(token):
            raise InvalidToken()
        
        token_data = await self.authenticate(token)
        
        if await self.token_blocklist.is_token_blocked(token_data['jti']):
            raise InvalidToken()
        
        return token_data

    def _token_valid(self, token: str) -> bool:
        token_data = decode_jwt_token(token)
        return token_data is not None

    async def authenticate(self, token):
        raise NotImplementedError('Please Override this method in child classes')


class AccessTokenBearer(BearerTokenAuth):
    async def authenticate(self, token):
        token_data = decode_jwt_token(token)
        if token_data and token_data.get('refresh'):
            raise AccessTokenRequired('Access token required, not refresh token.')
        return token_data


class RefreshTokenBearer(BearerTokenAuth):
    async def authenticate(self, token):
        token_data = decode_jwt_token(token)
        if token_data and not token_data.get('refresh'):
            raise RefreshTokenRequired('Refresh token required, not access token.')
        return token_data
