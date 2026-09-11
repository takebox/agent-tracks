"""CLI for tracks-ref library."""

import json
import sys
from pathlib import Path

import click

from .errors import TrackError
from .parser import read_properties
from .prompt import to_prompt
from .validator import validate


def _is_track_md_file(path: Path) -> bool:
    """Check if path points directly to a TRACK.md or track.md file."""
    return path.is_file() and path.name.lower() == "track.md"


@click.group()
@click.version_option()
def main():
    """Reference library for Agent Tracks."""
    pass


@main.command("validate")
@click.argument("track_path", type=click.Path(exists=True, path_type=Path))
def validate_cmd(track_path: Path):
    """Validate a track directory.

    Checks that the track has a valid TRACK.md with proper frontmatter,
    correct naming conventions, and required fields.

    Exit codes:
        0: Valid track
        1: Validation errors found
    """
    if _is_track_md_file(track_path):
        track_path = track_path.parent

    errors = validate(track_path)

    if errors:
        click.echo(f"Validation failed for {track_path}:", err=True)
        for error in errors:
            click.echo(f"  - {error}", err=True)
        sys.exit(1)
    else:
        click.echo(f"Valid track: {track_path}")


@main.command("read-properties")
@click.argument("track_path", type=click.Path(exists=True, path_type=Path))
def read_properties_cmd(track_path: Path):
    """Read and print track properties as JSON.

    Parses the YAML frontmatter from TRACK.md and outputs the
    properties as JSON.

    Exit codes:
        0: Success
        1: Parse error
    """
    try:
        if _is_track_md_file(track_path):
            track_path = track_path.parent

        props = read_properties(track_path)
        click.echo(json.dumps(props.to_dict(), indent=2))
    except TrackError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command("to-prompt")
@click.argument(
    "track_paths", type=click.Path(exists=True, path_type=Path), nargs=-1, required=True
)
def to_prompt_cmd(track_paths: tuple[Path, ...]):
    """Generate <available_tracks> XML for agent prompts.

    Accepts one or more track directories.

    Exit codes:
        0: Success
        1: Error
    """
    try:
        resolved_paths = []
        for track_path in track_paths:
            if _is_track_md_file(track_path):
                resolved_paths.append(track_path.parent)
            else:
                resolved_paths.append(track_path)

        output = to_prompt(resolved_paths)
        click.echo(output)
    except TrackError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
