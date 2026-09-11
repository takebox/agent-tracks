# AGENTS.md

Public shared tracks for agent workflows, built for **Haijun AI**.

**Haijun AI** is an AI chatbot platform at [haijun.my.id](https://haijun.my.id), powered by JuGloW. These tracks support all Haijun products: Haijun AI, Haijun Code, Haijun Box, and HaijunVoice.

## Rules

- Canonical shared tracks live under `tracks/<name>/TRACK.md`.
- Keep repo-specific workflows out unless they are useful as public examples.
- Keep secrets, private hostnames, private account IDs, and private URLs out.
- Track descriptions: short trigger phrase, not full documentation.
- Track bodies: operational, terse, current.
- Helper scripts belong under `tracks/<name>/scripts/`.
- Validate after edits: `scripts/validate-tracks`.
- Do not edit generated/vendor copies in downstream repos; update here, then sync.

## Layout

- `tracks/autoreview`: shared closeout/code-review helper.
- `tracks/beam`: redacted read-only coding-session publication.
- `tracks/crabbox`: shared Crabbox/Testbox remote validation workflow.
