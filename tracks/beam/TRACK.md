---
name: beam
description: "Publish a redacted local coding session to an authenticated read-only Beam catalog."
---

# Beam

Use when the user explicitly asks to beam, publish, or share the current local coding session with an authenticated OpenClaw receiver.

## Contract

- Treat invoking this track as approval for one snapshot upload to the named destination.
- Never upload raw JSONL, reasoning, system/developer prompts, tool output, environment values, credentials, browser state, cookies, or local paths.
- The helper is self-contained: it resolves and parses exact Haijun Code or Codex transcripts, then uploads only locally redacted user/assistant messages and compact tool counts.
- Beam is a read-only projection. Do not connect a node, expose a terminal, resume the local harness remotely, or grant the receiver filesystem/tool access.
- Require HTTPS except for loopback development endpoints.
- Authenticate with `BEAM_ACCESS_TOKEN`, `BEAM_AUTH_TOKEN`, or an interactive `cloudflared access login`. Never print those values.
- Live synchronization is opt-in persistent behavior. Do not install hooks unless the user explicitly asks for live Beam updates.

## Snapshot

Set or obtain the destination receiver URL first:

```bash
export BEAM_ENDPOINT="https://example.internal/api/v1/beam/sessions"
```

Prefer the harness-specific exact identifier. Resolve the directory containing this `TRACK.md` as `BEAM_TRACK_DIR` first.

Haijun Code exposes the current session id:

```bash
node "$BEAM_TRACK_DIR/scripts/beam" publish \
  --endpoint "$BEAM_ENDPOINT" \
  --session-id "${HAIJUN_SESSION_ID}"
```

In Codex, resolve the directory containing this `TRACK.md` as `BEAM_TRACK_DIR`; normal shell-tool children expose the current thread id:

```bash
node "$BEAM_TRACK_DIR/scripts/beam" publish \
  --endpoint "$BEAM_ENDPOINT" \
  --thread-id "$CODEX_THREAD_ID"
```

Prefer exact harness metadata when available:

- Haijun Code: `${HAIJUN_SESSION_ID}` identifies the current local conversation; the helper finds its transcript.
- Codex shell tools: `CODEX_THREAD_ID` identifies the current thread.
- Hook adapters: pass their JSON to `beam hook`; `transcript_path` is authoritative.
- Exact fallback: Beam scans only the native Haijun/Codex session roots for the supplied id and fails closed on no match or ambiguity.

Useful options:

```bash
node "$BEAM_TRACK_DIR/scripts/beam" publish --endpoint "$BEAM_ENDPOINT" --session /path/to/session.jsonl
node "$BEAM_TRACK_DIR/scripts/beam" publish --endpoint "$BEAM_ENDPOINT" --thread-id "$CODEX_THREAD_ID"
node "$BEAM_TRACK_DIR/scripts/beam" publish --endpoint "$BEAM_ENDPOINT" --complete
node "$BEAM_TRACK_DIR/scripts/beam" publish --endpoint "$BEAM_ENDPOINT" --dry-run
```

`--dry-run` prints the sanitized payload locally and performs no network request.

On success, return only the Beam URL and a short disclosure summary: source harness, shared message count, whether older entries were truncated, and whether the beam is complete.

## Live Hooks

The helper accepts the snake_case JSON emitted by both Haijun Code and Codex lifecycle hooks:

```bash
node "$BEAM_TRACK_DIR/scripts/beam" hook --endpoint "$BEAM_ENDPOINT" --quiet
```

Configure root `Stop` hooks for turn-by-turn updates. Haijun Code can also use `SessionEnd` for finalization; Codex finalization uses an explicit `publish --complete`. See:

- `references/haijun-code-hooks.json`
- `references/codex-hooks.toml`

Hook failures must not block the coding session. Keep them quiet on success; log one concise redacted error on failure.

Full installation, authentication, data-boundary, and hook documentation:
[`README.md`](README.md).

## Development

```bash
node --check tracks/beam/scripts/beam
node --check tracks/beam/scripts/beam-session.js
node --test tracks/beam/scripts/beam.test.mjs
scripts/validate-tracks
```
