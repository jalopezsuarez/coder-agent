# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Coder Agent is a **Markdown-only agent instruction set** — not a binary, service, or traditional software project. It turns any LLM-powered CLI (Claude Code, Gemini CLI, Codex CLI) into a disciplined developer that follows a Kanban workflow inside an Obsidian vault. There are no build, lint, or test commands.

## Single Source of Truth

`AG-CODER/AG-CODER.md` is the agent brain. All behavior, workflow rules, and memory system design live there. `AGENTS.md` and `GEMINI.md` are thin bridges that tell each CLI to read it. When modifying agent behavior, edit only `AG-CODER.md`.

## Repository Layout

- `AG-CODER/` — All agent files (instructions, templates, memory scaffolds)
  - `AG-CODER.md` — Complete agent instructions
  - `AGENTS.md` — Bridge for Claude Code / Codex CLI
  - `GEMINI.md` — Bridge for Gemini CLI
  - `TAREA-TEMPLATE.md` — Task note template
  - `Coder Board.md` — Empty Kanban board template (Obsidian Kanban plugin compatible)
  - `Coder Memory.md`, `architecture.md`, `modules.md`, `conventions.md`, `dependencies.md`, `knowledge-graph.md` — AI-optimized memory scaffolds
- `AG-CODER-v0.202604112034.zip` — Packaged release of the AG-CODER directory
- `README.md` — User-facing documentation

## How It Works When Deployed

Users copy the AG-CODER contents into their project root. On first run, the agent bootstraps a `Coder Factory/` directory with three subdirectories: `Coder Memory/` (AI knowledge base), `Coder Board/` (Kanban), and `Coder Notes/` (task notes). The workflow is: `create task` -> BACKLOG -> PLAN -> `plan tasks` -> REVIEW -> EXECUTION -> `execute tasks` -> TESTING -> DONE.

## Key Design Constraints

- **Incremental, append-only**: PLANNING #1 is never rewritten; PLANNING #2 is appended with deltas only.
- **Separated zones**: INSTRUCTIONS sections are human-exclusive (read-only for the agent). PLANNING and EXECUTION sections are agent-exclusive.
- **Token discipline**: Memory files are compressed for LLM consumption, not human readability. Updates are capped at ~2000 tokens.
- **Hierarchical memory loading**: Only `Coder Memory.md` is always loaded. Other files load on demand per phase (planning, execution).

## Versioning

Format: `v0.YYYYMMDDHHMM`. Current: **v0.202604112034**. When releasing, update the version timestamp in `AG-CODER.md` and the zip filename.

## Contributing

Edit `AG-CODER.md` for agent behavior changes. Update the version timestamp. The README in `AG-CODER/` mirrors the root README — keep both in sync.
