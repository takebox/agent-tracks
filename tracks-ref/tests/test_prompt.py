"""Tests for prompt module."""

from tracks_ref.prompt import to_prompt


def test_empty_list():
    result = to_prompt([])
    assert result == "<available_tracks>\n</available_tracks>"


def test_single_track(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
---
Body
""")
    result = to_prompt([track_dir])
    assert "<available_tracks>" in result
    assert "</available_tracks>" in result
    assert "<name>\nmy-track\n</name>" in result
    assert "<description>\nA test track\n</description>" in result
    assert "<location>" in result
    assert "TRACK.md" in result


def test_multiple_tracks(tmp_path):
    track_a = tmp_path / "track-a"
    track_a.mkdir()
    (track_a / "TRACK.md").write_text("""---
name: track-a
description: First track
---
Body
""")

    track_b = tmp_path / "track-b"
    track_b.mkdir()
    (track_b / "TRACK.md").write_text("""---
name: track-b
description: Second track
---
Body
""")

    result = to_prompt([track_a, track_b])
    assert result.count("<track>") == 2
    assert result.count("</track>") == 2
    assert "track-a" in result
    assert "track-b" in result


def test_special_characters_escaped(tmp_path):
    """XML special characters in description are escaped."""
    track_dir = tmp_path / "special-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: special-track
description: Use <foo> & <bar> tags
---
Body
""")
    result = to_prompt([track_dir])
    assert "&lt;foo&gt;" in result
    assert "&amp;" in result
    assert "&lt;bar&gt;" in result
    assert "<foo>" not in result
    assert "<bar>" not in result
