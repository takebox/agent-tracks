"""Tests for parser module."""

import pytest

from tracks_ref.parser import (
    ParseError,
    ValidationError,
    find_track_md,
    parse_frontmatter,
    read_properties,
)


def test_valid_frontmatter():
    content = """---
name: my-track
description: A test track
---
# My Track

Instructions here.
"""
    metadata, body = parse_frontmatter(content)
    assert metadata["name"] == "my-track"
    assert metadata["description"] == "A test track"
    assert "# My Track" in body


def test_missing_frontmatter():
    content = "# No frontmatter here"
    with pytest.raises(ParseError, match="must start with YAML frontmatter"):
        parse_frontmatter(content)


def test_unclosed_frontmatter():
    content = """---
name: my-track
description: A test track
"""
    with pytest.raises(ParseError, match="not properly closed"):
        parse_frontmatter(content)


def test_invalid_yaml():
    content = """---
name: [invalid
description: broken
---
Body here
"""
    with pytest.raises(ParseError, match="Invalid YAML"):
        parse_frontmatter(content)


def test_non_dict_frontmatter():
    content = """---
- just
- a
- list
---
Body
"""
    with pytest.raises(ParseError, match="must be a YAML mapping"):
        parse_frontmatter(content)


def test_read_valid_track(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
license: MIT
---
# My Track
""")
    props = read_properties(track_dir)
    assert props.name == "my-track"
    assert props.description == "A test track"
    assert props.license == "MIT"


def test_read_with_metadata(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
metadata:
  author: Test Author
  version: 1.0
---
Body
""")
    props = read_properties(track_dir)
    assert props.metadata == {"author": "Test Author", "version": "1.0"}


def test_missing_track_md(tmp_path):
    with pytest.raises(ParseError, match="TRACK.md not found"):
        read_properties(tmp_path)


def test_missing_name(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
description: A test track
---
Body
""")
    with pytest.raises(ValidationError, match="Missing required field.*name"):
        read_properties(track_dir)


def test_missing_description(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
---
Body
""")
    with pytest.raises(ValidationError, match="Missing required field.*description"):
        read_properties(track_dir)


def test_find_track_md_prefers_uppercase(tmp_path):
    """TRACK.md should be preferred over track.md when both exist."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("uppercase")
    (track_dir / "track.md").write_text("lowercase")
    result = find_track_md(track_dir)
    assert result is not None
    assert result.name == "TRACK.md"


def test_find_track_md_accepts_lowercase(tmp_path):
    """track.md should be accepted when TRACK.md doesn't exist."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "track.md").write_text("lowercase")
    result = find_track_md(track_dir)
    assert result is not None
    # Check case-insensitively since some filesystems are case-insensitive
    assert result.name.lower() == "track.md"


def test_find_track_md_returns_none_when_missing(tmp_path):
    """find_track_md should return None when no track.md exists."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    result = find_track_md(track_dir)
    assert result is None


def test_read_properties_with_lowercase_track_md(tmp_path):
    """read_properties should work with lowercase track.md."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "track.md").write_text("""---
name: my-track
description: A test track
---
# My Track
""")
    props = read_properties(track_dir)
    assert props.name == "my-track"
    assert props.description == "A test track"


def test_read_with_allowed_tools(tmp_path):
    """allowed-tools should be parsed into TrackProperties."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
allowed-tools: Bash(jq:*) Bash(git:*)
---
Body
""")
    props = read_properties(track_dir)
    assert props.allowed_tools == "Bash(jq:*) Bash(git:*)"
    # Verify to_dict outputs as "allowed-tools" (hyphenated)
    d = props.to_dict()
    assert d["allowed-tools"] == "Bash(jq:*) Bash(git:*)"
