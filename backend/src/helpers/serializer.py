from typing import List, Type, TypeVar, Union
from pydantic import BaseModel

from src.helpers.paginator import Paginator, CursorPaginator
from src.utils import encode_cursor

T = TypeVar('T', bound=BaseModel)


def serialize_model(data: Union[dict, List[dict]], model_type: Type[T]) -> Union[T, List[T]]:
    """
    A helper function that dynamically serializes data using the specified Pydantic model.

    Args:
        data: The data to serialize (can be a single dict or a Paginator/CursorPaginator obj from src.paginator.Paginator/CursorPaginator).
        model_type: The Pydantic model class to use for serialization.

    Returns:
        A serialized model instance or a list of model instances.
    """
    if isinstance(data, Paginator):
        data.items = [model_type.model_validate(item) for item in data.items]
        return data

    if isinstance(data, CursorPaginator):
        data.items = [model_type.model_validate(item) for item in data.items]
        data.next_cursor = encode_cursor(data.next_cursor) if data.next_cursor else None
        return data

    if isinstance(data, list):
        return [model_type.model_validate(each) for each in data]
    
    return model_type.model_validate(data)
