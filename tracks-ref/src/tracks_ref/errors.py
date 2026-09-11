"""Track-related exceptions."""


class TrackError(Exception):
    """Base exception for all track-related errors."""

    pass


class ParseError(TrackError):
    """Raised when TRACK.md parsing fails."""

    pass


class ValidationError(TrackError):
    """Raised when track properties are invalid.

    Attributes:
        errors: List of validation error messages (may contain just one)
    """

    def __init__(self, message: str, errors: list[str] | None = None):
        super().__init__(message)
        self.errors = errors if errors is not None else [message]
