from typing import Any, Optional, Dict, Union
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.helpers.paginator import Paginator, CursorPaginator


class ApiResponser(JSONResponse):
    @classmethod
    def success_response(
        cls,
        data: Optional[Any] = None,
        message: str = 'Request was successful',
        status_code: int = 200,
        metadata: Optional[Dict[str, Any]] = None,
        paginated: bool = False,
    ) -> 'ApiResponser':
        response_content = {
            'success': True,
            'message': message,
        }
        if paginated and isinstance(data, Paginator):
            response_content['data'] = jsonable_encoder(data.items)
            response_content['metadata'] = data.to_dict()
        elif paginated and isinstance(data, CursorPaginator):
            response_content['data'] = jsonable_encoder(data.items)
            response_content['metadata'] = data.to_dict()
        else:
            response_content['data'] = jsonable_encoder(data)
            response_content['metadata'] = metadata
        
        return cls(content=response_content, status_code=status_code)

    @classmethod
    def error_response(
        cls,
        message: str = 'An error occurred',
        status_code: int = 400,
        error_details: Optional[Union[str, Dict[str, Any]]] = None,
    ) -> 'ApiResponser':
        response_content = {
            'success': False,
            'message': message,
            'error_details': error_details,
        }
        return cls(content=response_content, status_code=status_code)
