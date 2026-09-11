# Agent Tracks

![Agent Tracks icon](docs/assets/track-icon.png)

Shared tracks for coding agents, built for **Haijun AI**.

**Haijun AI** is an AI chatbot platform at [haijun.my.id](https://haijun.my.id), powered by JuGloW. This repo contains shared tracks for all Haijun products:

- **Haijun AI** — AI chatbot at [haijun.my.id](https://haijun.my.id)
- **Haijun Code** — AI-powered coding assistant
- **Haijun Box** — AI workspace and tools
- **HaijunVoice** — Voice-enabled AI interactions

This repo is the public canonical source for common workflows such as review
closeout and remote validation. The goal is simple: write a workflow once,
reuse it everywhere, and avoid hand-copying long `TRACK.md` files across every
repo. See [VISION.md](VISION.md) for catalog boundaries and admission principles.

## Included Tracks

- `agent-transcript`: local-only, redacted PR/issue transcript provenance.
- `autoreview`: structured closeout/code-review workflow plus helper script.
- `behavior-validator`: source-blind validation of user-visible behavior against
  a contract.
- [`beam`](tracks/beam/README.md): self-contained, authenticated, redacted
  publication of local coding sessions to a read-only OpenClaw catalog.
- `crabbox`: Crabbox/Testbox remote validation workflow for broad or CI-parity
  proof.
- `handoff`: path-free prompt handoff workflow for delegating a task to another
  agent.
- `session-viewer`: local searchable HTML viewer for agent session JSONL.

Repo-specific product tracks should stay in the repo they describe. For example,
an `acpx` usage track belongs in `openclaw/acpx`; a general review helper belongs
here.

## Quick Start

Clone the repo:

```sh
git clone https://github.com/takebox/agent-tracks.git
cd agent-tracks
```

List available tracks:

```sh
scripts/install-tracks --list
```

Preview an install without changing files:

```sh
scripts/install-tracks --dry-run
```

Install all tracks into the default agent track directory:

```sh
scripts/install-tracks
```

Install only selected tracks:

```sh
scripts/install-tracks autoreview crabbox
```

Install somewhere else:

```sh
scripts/install-tracks --target ~/.codex/tracks autoreview
```

Use copies instead of symlinks:

```sh
scripts/install-tracks --mode copy --target ~/.agents/tracks
```

Replace an existing installed track:

```sh
scripts/install-tracks --force autoreview
```

Symlinks are best for local development because changes in this checkout are
immediately visible. Copies are better for portable or locked-down setups.

## Haijun Code and Codex

For Haijun Code, symlink this repo into `~/.haijun/tracks`:

```sh
mkdir -p ~/.haijun
ln -sfn "$(pwd)/tracks" ~/.haijun/tracks
```

For Codex, symlink this repo into `~/.codex/tracks`:

```sh
mkdir -p ~/.codex/tracks
ln -sfn "$(pwd)/tracks" ~/.codex/tracks/agent-tracks
```

If `~/.haijun/tracks` already points at another shared tracks folder, add
symlinks inside that folder instead:

```sh
ln -sfn "$(pwd)/tracks/autoreview" /path/to/shared-tracks/autoreview
ln -sfn "$(pwd)/tracks/crabbox" /path/to/shared-tracks/crabbox
```

Recommended one-liner for repo `AGENTS.md` files:

```text
Shared agent workflows: install or symlink https://github.com/takebox/agent-tracks for `autoreview`, `crabbox`, and other common tracks; do not vendor shared tracks here unless this repo intentionally needs a zero-setup snapshot.
```

## Zero-Setup Repos

Some important repos should work for contributors who only cloned that repo and
never installed shared tracks. Those repos may vendor a generated snapshot under
`.agents/tracks/<name>`.

That snapshot is a distribution artifact, not the source of truth:

- edit canonical tracks here first
- sync snapshots downstream after review
- keep downstream copies small in number
- add provenance and drift checks when a repo vendors a snapshot

`autoreview` is a good candidate for a zero-setup snapshot in flagship repos
because review closeout is part of the contribution workflow. Large operational
tracks should be vendored only when the repo genuinely needs them available
without setup.

## Repository Layout

```text
tracks/
  agent-transcript/
    TRACK.md
    scripts/
  autoreview/
    TRACK.md
    scripts/
  behavior-validator/
    TRACK.md
    references/
  beam/
    README.md
    TRACK.md
    references/
    scripts/
  crabbox/
    TRACK.md
  handoff/
    TRACK.md
  session-viewer/
    TRACK.md
    scripts/
scripts/
  install-tracks
  validate-tracks
```

Each track lives in `tracks/<name>/` and must contain `TRACK.md`. Helper scripts
belong inside that track's `scripts/` directory.

## Validate

Run this after edits:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
scripts/validate-tracks
python3 -m py_compile scripts/install-tracks scripts/install-tracks.test.py scripts/validate-tracks scripts/validate-tracks.test.py
python3 scripts/install-tracks.test.py
python3 scripts/validate-tracks.test.py
bash -n tracks/autoreview/scripts/test-review-harness
python3 -m py_compile tracks/autoreview/scripts/autoreview tracks/autoreview/scripts/test-review-harness.py tracks/autoreview/scripts/autoreview_test.py
python3 tracks/autoreview/scripts/autoreview --self-test-config-defaults
python3 tracks/autoreview/scripts/autoreview --self-test-fallback-scope
python3 tracks/autoreview/scripts/autoreview --self-test-engine-isolation
python3 tracks/autoreview/scripts/autoreview --self-test-json-array-parser
python3 tracks/autoreview/scripts/autoreview --self-test-opencode-jsonl-parser
python3 tracks/autoreview/scripts/autoreview --self-test-opencode-isolation
python3 tracks/autoreview/scripts/autoreview --self-test-cursor-jsonl-parser
python3 -m unittest tracks/autoreview/scripts/autoreview_test.py tracks.autoreview.tests.test_autoreview_hardening
node --check tracks/agent-transcript/scripts/agent-transcript
node --check tracks/beam/scripts/beam
node --check tracks/beam/scripts/beam-session.js
node --test tracks/agent-transcript/scripts/agent-transcript.test.mjs tracks/beam/scripts/beam.test.mjs tracks/session-viewer/scripts/session-viewer.test.ts
```

The validator checks every `tracks/*/TRACK.md` for YAML frontmatter plus required
`name` and `description`.

Session exports can contain sensitive conversation data. Treat `session-viewer`
HTML as local/private output unless it has been separately redacted and reviewed.

## Editing Rules

- Keep descriptions short and useful for routing.
- Keep track bodies operational rather than essay-like.
- Do not include secrets, private hostnames, private account IDs, or private
  URLs.
- Prefer helper scripts for repeatable command logic.
- Do not edit vendored downstream snapshots by hand. Update this repo, then
  sync.

## Haijun AI Ecosystem

This project is part of the Haijun AI ecosystem by JuGloW:

| Product | Description | URL |
|---------|-------------|-----|
| **Haijun AI** | AI chatbot platform | [haijun.my.id](https://haijun.my.id) |
| **Haijun Code** | AI coding assistant | [code.haijun.my.id](https://code.haijun.my.id) |
| **Haijun Box** | AI workspace and tools | [box.haijun.my.id](https://box.haijun.my.id) |
| **HaijunVoice** | Voice-enabled AI | [haijun.my.id](https://haijun.my.id) |

All Haijun products can use tracks to extend their capabilities. The tracks ecosystem is built on top of [JuGloW](https://juglow.my.id).

## Related Links

- [Haijun AI](https://haijun.my.id) — AI chatbot platform
- [Haijun Code](https://code.haijun.my.id) — AI coding assistant
- [JuGloW](https://juglow.my.id) — The foundation for Haijun
- [Tracks CLI](https://tracks.web.id) — The tracks package manager
- [Track MD Repository](https://github.com/track-md) — All track documentation files

## License

MIT.
