"""Tests for validator module."""

from tracks_ref.validator import validate


def test_valid_track(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
---
# My Track
""")
    errors = validate(track_dir)
    assert errors == []


def test_nonexistent_path(tmp_path):
    errors = validate(tmp_path / "nonexistent")
    assert len(errors) == 1
    assert "does not exist" in errors[0]


def test_not_a_directory(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("test")
    errors = validate(file_path)
    assert len(errors) == 1
    assert "Not a directory" in errors[0]


def test_missing_track_md(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    errors = validate(track_dir)
    assert len(errors) == 1
    assert "Missing required file: TRACK.md" in errors[0]


def test_invalid_name_uppercase(tmp_path):
    track_dir = tmp_path / "MyTrack"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: MyTrack
description: A test track
---
Body
""")
    errors = validate(track_dir)
    assert any("lowercase" in e for e in errors)


def test_name_too_long(tmp_path):
    long_name = "a" * 70  # Exceeds 64 char limit
    track_dir = tmp_path / long_name
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text(f"""---
name: {long_name}
description: A test track
---
Body
""")
    errors = validate(track_dir)
    assert any("exceeds" in e and "character limit" in e for e in errors)


def test_name_leading_hyphen(tmp_path):
    track_dir = tmp_path / "-my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: -my-track
description: A test track
---
Body
""")
    errors = validate(track_dir)
    assert any("cannot start or end with a hyphen" in e for e in errors)


def test_name_consecutive_hyphens(tmp_path):
    track_dir = tmp_path / "my--track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my--track
description: A test track
---
Body
""")
    errors = validate(track_dir)
    assert any("consecutive hyphens" in e for e in errors)


def test_name_invalid_characters(tmp_path):
    track_dir = tmp_path / "my_track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my_track
description: A test track
---
Body
""")
    errors = validate(track_dir)
    assert any("invalid characters" in e for e in errors)


def test_name_directory_mismatch(tmp_path):
    track_dir = tmp_path / "wrong-name"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: correct-name
description: A test track
---
Body
""")
    errors = validate(track_dir)
    assert any("must match track name" in e for e in errors)


def test_unexpected_fields(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
unknown_field: should not be here
---
Body
""")
    errors = validate(track_dir)
    assert any("Unexpected fields" in e for e in errors)


def test_valid_with_all_fields(tmp_path):
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
license: MIT
metadata:
  author: Test
---
Body
""")
    errors = validate(track_dir)
    assert errors == []


def test_allowed_tools_accepted(tmp_path):
    """allowed-tools is accepted (experimental feature)."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
allowed-tools: Bash(jq:*) Bash(git:*)
---
Body
""")
    errors = validate(track_dir)
    assert errors == []


def test_i18n_chinese_name(tmp_path):
    """Chinese characters are allowed in track names."""
    track_dir = tmp_path / "赛道"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: 赛道
description: A track with Chinese name
---
Body
""")
    errors = validate(track_dir)
    assert errors == []


def test_i18n_russian_name_with_hyphens(tmp_path):
    """Russian names with hyphens are allowed."""
    track_dir = tmp_path / "мой-трек"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: мой-трек
description: A track with Russian name
---
Body
""")
    errors = validate(track_dir)
    assert errors == []


def test_i18n_russian_lowercase_valid(tmp_path):
    """Russian lowercase names should be accepted."""
    track_dir = tmp_path / "трек"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: трек
description: A track with Russian lowercase name
---
Body
""")
    errors = validate(track_dir)
    assert errors == []


def test_i18n_russian_uppercase_rejected(tmp_path):
    """Russian uppercase names should be rejected."""
    track_dir = tmp_path / "ТРЕК"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: ТРЕК
description: A track with Russian uppercase name
---
Body
""")
    errors = validate(track_dir)
    assert any("lowercase" in e for e in errors)


def test_description_too_long(tmp_path):
    """Description exceeding 1024 chars should fail."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    long_desc = "x" * 1100
    (track_dir / "TRACK.md").write_text(f"""---
name: my-track
description: {long_desc}
---
Body
""")
    errors = validate(track_dir)
    assert any("exceeds" in e and "1024" in e for e in errors)


def test_valid_compatibility(tmp_path):
    """Valid compatibility field should be accepted."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text("""---
name: my-track
description: A test track
compatibility: Requires Python 3.11+
---
Body
""")
    errors = validate(track_dir)
    assert errors == []


def test_compatibility_too_long(tmp_path):
    """Compatibility exceeding 500 chars should fail."""
    track_dir = tmp_path / "my-track"
    track_dir.mkdir()
    long_compat = "x" * 550
    (track_dir / "TRACK.md").write_text(f"""---
name: my-track
description: A test track
compatibility: {long_compat}
---
Body
""")
    errors = validate(track_dir)
    assert any("exceeds" in e and "500" in e for e in errors)


def test_nfkc_normalization(tmp_path):
    """Track names are NFKC normalized before validation.

    The name 'café' can be represented two ways:
    - Precomposed: 'café' (4 chars, 'é' is U+00E9)
    - Decomposed: 'café' (5 chars, 'e' + combining acute U+0301)

    NFKC normalizes both to the precomposed form.
    """
    # Use decomposed form: 'cafe' + combining acute accent (U+0301)
    decomposed_name = "cafe\u0301"  # 'café' with combining accent
    composed_name = "café"  # precomposed form

    # Directory uses composed form, TRACK.md uses decomposed - should match after normalization
    track_dir = tmp_path / composed_name
    track_dir.mkdir()
    (track_dir / "TRACK.md").write_text(f"""---
name: {decomposed_name}
description: A test track
---
Body
""")
    errors = validate(track_dir)
    assert errors == [], f"Expected no errors, got: {errors}"
