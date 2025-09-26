from typing import Optional

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    APIKeyHeader,
)


class Auth:

    @classmethod
    def scheme(self, auth_type: str) -> Optional[HTTPBearer | HTTPBasic | APIKeyHeader]:
        if auth_type == 'bearer':
            return HTTPBearer
        elif auth_type == 'basic':
            return HTTPBasic
        elif auth_type == 'apikey':
            return APIKeyHeader(name='X-API-KEY')
        else:
            raise ValueError(f'Unsupported auth type: {auth_type}')
