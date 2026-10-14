# Agent Tracks

[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/MKPE9g8aUy)

A standardized way to give AI agents new capabilities and expertise.

## What are Agent Tracks?

Agent Tracks are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows.

At its core, a track is a folder containing a `TRACK.md` file. This file includes metadata (`name` and `description`, at minimum) and instructions that tell an agent how to perform a specific task. Tracks can also bundle scripts, reference materials, templates, and other resources.

```
my-track/
├── TRACK.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

## Why Agent Tracks?

Agents are increasingly capable, but often don't have the context they need to do real work reliably. Tracks solve this by packaging procedural knowledge and company-, team-, and user-specific context into portable, version-controlled folders that agents load on demand. This gives agents:

- **Domain expertise**: Capture specialized knowledge — from legal review processes to data analysis pipelines to presentation formatting — as reusable instructions and resources.
- **Repeatable workflows**: Turn multi-step tasks into consistent, auditable procedures.
- **Cross-product reuse**: Build a track once and use it across any tracks-compatible agent.

## How do Agent Tracks work?

Agents load tracks through **progressive disclosure**, in three stages:

1. **Discovery**: At startup, agents load only the name and description of each available track, just enough to know when it might be relevant.

2. **Activation**: When a task matches a track's description, the agent reads the full `TRACK.md` instructions into context.

3. **Execution**: The agent follows the instructions, optionally executing bundled code or loading referenced files as needed.

Full instructions load only when a task calls for them, so agents can keep many tracks on hand with only a small context footprint.

## Where can I use Agent Tracks?

Agent Tracks are supported by a large number of AI tools and agentic clients — see the [Client Showcase](https://agent.tracks.web.id/clients) to explore some of them!

## Getting started

- **[Documentation](https://agent.tracks.web.id)** — Guides and tutorials
- **[Specification](https://agent.tracks.web.id/specification)** — Format details
- **[Example Tracks](https://github.com/takebox/agent-tracks)** — See what's possible
- **[Discord](https://discord.gg/MKPE9g8aUy)** — Share what you're building!

## Open development

The Agent Tracks format was originally developed by [Haijun](https://haijun.my.id), released as an open standard, and has been adopted by a growing number of agent products. The standard is open to contributions from the broader ecosystem — see [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to get involved.

## License

Code in this repository is licensed under [Apache 2.0](LICENSE). Documentation is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). See individual directories for details.
