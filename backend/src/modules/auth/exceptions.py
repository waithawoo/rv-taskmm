from src.exceptions import AppException


class InvalidToken(AppException):
    """Invalid or Expired token."""

    pass


class RefreshTokenRequired(AppException):
    """Invalid Username and Password."""

    pass


class AccessTokenRequired(AppException):
    """Access token required."""

    pass


class InsufficientPermission(AppException):
    """Insufficient permission."""

    pass


class AccountNotVerified(AppException):
    """Account not verified."""

    pass


class InvalidCredentials(AppException):
    """Invalid credentials."""

    pass


class UserAlreadyExists(AppException):
    """User is already existed."""

    pass


class UserNotFound(AppException):
    """User Not Found."""

    pass
