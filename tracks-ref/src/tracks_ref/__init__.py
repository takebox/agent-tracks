"""Reference library for Agent Tracks."""

from .errors import ParseError, TrackError, ValidationError
from .models import TrackProperties
from .parser import find_track_md, read_properties
from .prompt import to_prompt
from .validator import validate

__all__ = [
    "TrackError",
    "ParseError",
    "ValidationError",
    "TrackProperties",
    "find_track_md",
    "validate",
    "read_properties",
    "to_prompt",
]

__version__ = "0.1.0"
