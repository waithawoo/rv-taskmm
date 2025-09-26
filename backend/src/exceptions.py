import importlib
import inspect
import logging
from typing import List, Dict

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.helpers.response import ApiResponser

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for global errors."""
    def __init__(self, message=None):
        if not message:
            message = self.__class__.__doc__.strip() if self.__class__.__doc__ else 'An error occurred'
        super().__init__(message)
        self.message = message


class ValidationException(Exception):
    """This is the base class for all custom ValidationError."""
    def __init__(self, message=None, details=None, code=None):
        if not message:
            message = 'A validation error occurred'
        
        super().__init__(message)
        
        self.message = message
        self.details = details
        self.code = code

    def __str__(self):
        error_message = f'Error: {self.message}'
        if self.details:
            error_message += f' | Details: {self.details}'
        if self.code:
            error_message += f' | Code: {self.code}'
        return error_message


# Global exception handler for custom application exceptions
async def global_exception_handler(request: Request, exc: AppException):
    logger.error(f'GlobalAppException {str(exc)}')
    
    return ApiResponser.error_response(
        message=f'{str(exc)}',
        status_code=status.HTTP_400_BAD_REQUEST,
    )


# Global custom validation exception handler for custom validation exceptions
async def global_validation_exception_handler(request: Request, exc: ValidationException):    
    return ApiResponser.error_response(
        message=f'{str(exc.message)}',
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_details=exc.details
    )


def format_validation_errors(errors: List[Dict]) -> List[Dict]:
    """
    Format validation errors for consistent API responses.

    Args:
        errors (List[Dict]): List of raw validation errors from FastAPI.

    Returns:
        List[Dict]: Formatted validation errors.
    """
    formatted = []
    for error in errors:
        formatted.append({
            'field': ' '.join(error['loc'][1:]),
            'error': error['msg'].replace('Value error, ', '')
        })
    return formatted


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for validation exceptions.
    """
    raw_errors = exc.errors()
    formatted_errors = format_validation_errors(raw_errors)
    logger.error(f'ValidationError : {str(exc)}')

    return ApiResponser.error_response(
        message='Validation Failed',
        status_code=422,
        error_details={'validationErrors': formatted_errors},
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler for HTTP exceptions.
    """
    logger.error(f'HTTPError : {str(exc)}')
    return ApiResponser.error_response(
        message=exc.detail, 
        status_code=exc.status_code
    )


# Register all exception handlers
def register_exceptions(app: FastAPI):
    """Register global exception handlers."""
    app.add_exception_handler(AppException, global_exception_handler)
    app.add_exception_handler(ValidationException, global_validation_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
