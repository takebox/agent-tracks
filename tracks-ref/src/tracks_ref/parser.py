"""YAML frontmatter parsing for TRACK.md files."""

from pathlib import Path
from typing import Optional

import strictyaml

from .errors import ParseError, ValidationError
from .models import TrackProperties


def find_track_md(track_dir: Path) -> Optional[Path]:
    """Find the TRACK.md file in a track directory.

    Prefers TRACK.md (uppercase) but accepts track.md (lowercase).

    Args:
        track_dir: Path to the track directory

    Returns:
        Path to the TRACK.md file, or None if not found
    """
    for name in ("TRACK.md", "track.md"):
        path = track_dir / name
        if path.exists():
            return path
    return None


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from TRACK.md content.

    Args:
        content: Raw content of TRACK.md file

    Returns:
        Tuple of (metadata dict, markdown body)

    Raises:
        ParseError: If frontmatter is missing or invalid
    """
    if not content.startswith("---"):
        raise ParseError("TRACK.md must start with YAML frontmatter (---)")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ParseError("TRACK.md frontmatter not properly closed with ---")

    frontmatter_str = parts[1]
    body = parts[2].strip()

    try:
        parsed = strictyaml.load(frontmatter_str)
        metadata = parsed.data
    except strictyaml.YAMLError as e:
        raise ParseError(f"Invalid YAML in frontmatter: {e}")

    if not isinstance(metadata, dict):
        raise ParseError("TRACK.md frontmatter must be a YAML mapping")

    if "metadata" in metadata and isinstance(metadata["metadata"], dict):
        metadata["metadata"] = {str(k): str(v) for k, v in metadata["metadata"].items()}

    return metadata, body


def read_properties(track_dir: Path) -> TrackProperties:
    """Read track properties from TRACK.md frontmatter.

    This function parses the frontmatter and returns properties.
    It does NOT perform full validation. Use validate() for that.

    Args:
        track_dir: Path to the track directory

    Returns:
        TrackProperties with parsed metadata

    Raises:
        ParseError: If TRACK.md is missing or has invalid YAML
        ValidationError: If required fields (name, description) are missing
    """
    track_dir = Path(track_dir)
    track_md = find_track_md(track_dir)

    if track_md is None:
        raise ParseError(f"TRACK.md not found in {track_dir}")

    content = track_md.read_text()
    metadata, _ = parse_frontmatter(content)

    if "name" not in metadata:
        raise ValidationError("Missing required field in frontmatter: name")
    if "description" not in metadata:
        raise ValidationError("Missing required field in frontmatter: description")

    name = metadata["name"]
    description = metadata["description"]

    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Field 'name' must be a non-empty string")
    if not isinstance(description, str) or not description.strip():
        raise ValidationError("Field 'description' must be a non-empty string")

    return TrackProperties(
        name=name.strip(),
        description=description.strip(),
        license=metadata.get("license"),
        compatibility=metadata.get("compatibility"),
        allowed_tools=metadata.get("allowed-tools"),
        metadata=metadata.get("metadata"),
    )
