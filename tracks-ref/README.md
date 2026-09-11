# tracks-ref

Reference library for Agent Tracks.

> [!IMPORTANT]
> This library is intended for demonstration purposes only. It is not meant to be used in production.

## Installation

### macOS / Linux

Using pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or using [uv](https://docs.astral.sh/uv/):

```bash
uv sync
source .venv/bin/activate
```

### Windows

Using pip (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

Using pip (Command Prompt):

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -e .
```

Or using [uv](https://docs.astral.sh/uv/):

```powershell
uv sync
.venv\Scripts\Activate.ps1
```

After installation, the `tracks-ref` executable will be available on your `PATH` (within the activated virtual environment).

## Usage

### CLI

```bash
# Validate a track
tracks-ref validate path/to/track

# Read track properties (outputs JSON)
tracks-ref read-properties path/to/track

# Generate <available_tracks> XML for agent prompts
tracks-ref to-prompt path/to/track-a path/to/track-b
```

### Python API

```python
from pathlib import Path
from tracks_ref import validate, read_properties, to_prompt

# Validate a track directory
problems = validate(Path("my-track"))
if problems:
    print("Validation errors:", problems)

# Read track properties
props = read_properties(Path("my-track"))
print(f"Track: {props.name} - {props.description}")

# Generate prompt for available tracks
prompt = to_prompt([Path("track-a"), Path("track-b")])
print(prompt)
```

## Agent Prompt Integration

Use `to-prompt` to generate the suggested `<available_tracks>` XML block for your agent's system prompt. This format is recommended for agent models, but Track Clients may choose to format it differently based on the model being used.

```xml
<available_tracks>
<track>
<name>
my-track
</name>
<description>
What this track does and when to use it
</description>
<location>
/path/to/my-track/TRACK.md
</location>
</track>
</available_tracks>
```

The `<location>` element tells the agent where to find the full track instructions.

## License

Apache 2.0
