from fastapi import Depends, Request
from fastapi.security.http import HTTPAuthorizationCredentials


class AuthHandler:
    def __init__(self, scheme):
        self._scheme = scheme
    
    @property
    def as_dependency(self):
        return Depends(self._scheme())
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        token_data = await self._scheme(request)
        return token_data
