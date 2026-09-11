"""Generate <available_tracks> XML prompt block for agent system prompts."""

import html
from pathlib import Path

from .parser import find_track_md, read_properties


def to_prompt(track_dirs: list[Path]) -> str:
    """Generate the <available_tracks> XML block for inclusion in agent prompts.

    This XML format is what we use and recommend for agent models.
    Track Clients may format track information differently to suit their
    models or preferences.

    Args:
        track_dirs: List of paths to track directories

    Returns:
        XML string with <available_tracks> block containing each track's
        name, description, and location.

    Example output:
        <available_tracks>
        <track>
        <name>pdf-reader</name>
        <description>Read and extract text from PDF files</description>
        <location>/path/to/pdf-reader/TRACK.md</location>
        </track>
        </available_tracks>
    """
    if not track_dirs:
        return "<available_tracks>\n</available_tracks>"

    lines = ["<available_tracks>"]

    for track_dir in track_dirs:
        track_dir = Path(track_dir).resolve()
        props = read_properties(track_dir)

        lines.append("<track>")
        lines.append("<name>")
        lines.append(html.escape(props.name))
        lines.append("</name>")
        lines.append("<description>")
        lines.append(html.escape(props.description))
        lines.append("</description>")

        track_md_path = find_track_md(track_dir)
        lines.append("<location>")
        lines.append(str(track_md_path))
        lines.append("</location>")

        lines.append("</track>")

    lines.append("</available_tracks>")

    return "\n".join(lines)
