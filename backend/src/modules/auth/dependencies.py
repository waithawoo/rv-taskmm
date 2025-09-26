from typing import Any, List
from fastapi import Depends, Request

from src.modules.user.models import User
from .services import AuthService
from .exceptions import (
    InsufficientPermission
)
from .schemes.bearer import AccessTokenBearer, RefreshTokenBearer
from .handlers import AuthHandler

access_token_handler = AuthHandler(AccessTokenBearer).as_dependency
refresh_token_handler = AuthHandler(RefreshTokenBearer).as_dependency

user_service = AuthService(User)


async def get_current_user(request: Request, token_details: dict = access_token_handler):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(request.state.db, user_email)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()
