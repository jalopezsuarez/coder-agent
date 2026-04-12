<p align="center">
  <img src="https://img.shields.io/badge/version-0.202604112034-blue?style=flat-square" alt="version" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license" />
  <img src="https://img.shields.io/badge/files-Markdown%20only-orange?style=flat-square" alt="markdown" />
</p>

<h1 align="center">🤖 Coder Agent</h1>

<p align="center">
  <strong>A production-grade AI coding agent that builds an optimized context memory — graphs, architecture, connections & tech — and accompanies you through the full project lifecycle.</strong><br/>
  Kanban-driven workflow · AI-optimized memory system · Works with any LLM CLI.
</p>

<p align="center">
  <img src="coder-agent.png" alt="Coder Agent" width="400"/>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-memory-system">Memory System</a> •
  <a href="#-cli-compatibility">CLI Compatibility</a>
</p>

---

## What is Coder?

Coder is an **agent instruction set** that turns any LLM CLI into a disciplined software developer. It operates through Markdown files — compatible with the Obsidian Kanban plugin, but fully usable standalone — following a strict Kanban workflow with human-in-the-loop review cycles.

**The key idea:** Coder doesn't just write code. It builds and maintains an AI-optimized context memory across your entire project: knowledge graphs, architectural decisions, technology stack, feature connections, and system relationships — all compacted into versioned Markdown notes designed for maximum LLM comprehension.

You manage a Kanban board. Coder reads the board, plans tasks, writes code, tracks bugs, and keeps the knowledge graph up to date — all through versioned, incremental Markdown notes. You stay in control at every step.

### Why Coder?

- **Zero infrastructure** — No servers, no databases, no API keys beyond your CLI. Just Markdown files.
- **Human-in-the-loop** — Every plan goes through your review before any code is written.
- **Full traceability** — Every decision, every change, every iteration is versioned and documented.
- **Token-efficient memory** — AI-optimized knowledge base with hierarchical loading, semantic compression, and incremental updates.
- **CLI-agnostic** — Works with Claude Code, Gemini CLI, Codex CLI, or any agent that reads instruction files.

---

## 🚀 Quick Start

### 1. Clone into your project

```bash
git clone https://github.com/jalopezsuarez/coder-agent.git
cp -r coder-agent/{CODER.md,AGENTS.md,GEMINI.md,.claude,Coder\ Factory,templates} /path/to/your/project/
```

Or simply copy the files manually into your project root.

### 2. Launch your CLI

```bash
# Claude Code
claude

# Gemini CLI
gemini

# OpenAI Codex CLI
codex
```

### 3. Start working

```
> create task Implement user authentication with JWT
> plan tasks
> execute tasks
```

That's it. Coder will:
1. **Auto-detect** that the structure doesn't exist and create it.
2. **Auto-index** your project into an AI-optimized knowledge base.
3. **Create the task**, plan it, and wait for your review.

---

## 🔄 How It Works

```
 You                          Coder                        Project
  │                             │                             │
  │  "create task X"            │                             │
  │────────────────────────────>│                             │
  │                             │──── create note ──────────> │
  │                             │──── add to BACKLOG ───────> │
  │                             │                             │
  │  move task to PLAN          │                             │
  │────────────────────────────>│                             │
  │                             │                             │
  │  "plan tasks"               │                             │
  │────────────────────────────>│                             │
  │                             │──── read memory ──────────> │
  │                             │──── write PLANNING #1 ────> │
  │                             │──── move to REVIEW ───────> │
  │                             │                             │
  │  review plan                │                             │
  │  write INSTRUCTIONS #1      │                             │
  │  move back to PLAN          │                             │
  │────────────────────────────>│                             │
  │                             │                             │
  │  "plan tasks"               │                             │
  │────────────────────────────>│                             │
  │                             │──── write PLANNING #2 ────> │
  │                             │──── move to REVIEW ───────> │
  │                             │                             │
  │  approve → move to EXECUTION│                             │
  │────────────────────────────>│                             │
  │                             │                             │
  │  "execute tasks"            │                             │
  │────────────────────────────>│                             │
  │                             │──── implement code ───────> │
  │                             │──── write EXECUTION #1 ───> │
  │                             │──── move to TESTING ──────> │
  │                             │                             │
  │  validate → DONE ✅         │                             │
  └─────────────────────────────┘                             │
```

### Kanban Columns

| Column | Owner | What happens |
|--------|-------|-------------|
| `BACKLOG` | You / Coder | Tasks created, waiting to be prioritized |
| `PLAN` | Coder | Coder generates a detailed plan |
| `REVIEW` | You | You review the plan, add feedback |
| `EXECUTION` | Coder | Coder writes the actual code |
| `TESTING` | You | You validate the implementation |
| `DONE` | You | Task completed |

### Task Notes

Every task gets a dedicated note with three strictly separated zones:

```markdown
## INSTRUCTIONS (Human Zone)    ← You write here
### INSTRUCTIONS #1 — 2026-04-11
- Your feedback and changes...

## PLANNING (Coder Zone)        ← Coder writes here
### PLANNING #1 — 2026-04-11
- Objective, analysis, action plan, files affected...

## EXECUTION (Coder Zone)       ← Coder writes here
### EXECUTION #1 — 2026-04-11
- Summary, changes made, technical decisions...
```

All sections are **versioned and incremental**. `PLANNING #1` is never modified — `PLANNING #2` is appended with only the delta.

---

## ⚡ Commands

| Command | Description |
|---------|-------------|
| `create task <description>` | Create a new task in BACKLOG with an associated note |
| `create task urgent <description>` | Same, with `#urgent` priority tag |
| `plan tasks` | Generate plans for all tasks in the PLAN column |
| `execute tasks` | Implement code for all tasks in the EXECUTION column |
| `status` | Show a summary of the Kanban board |
| `update memory` | Re-index the project and update the knowledge base |

### Tags

| Tag | Effect |
|-----|--------|
| `#coder` | Task assigned to the agent |
| `#urgent` | Processed first |
| `#blocked` | Agent will not touch it |

---

## 🧠 Memory System

Coder maintains an **AI-optimized knowledge base** designed for maximum information density and minimum token usage. It is NOT meant for human reading — it's structured for LLM consumption.

### Architecture

```
coder-factory/
└── coder-memory/
    ├── memory.md      ← Always loaded (~50-100 lines)
    ├── architecture.md      ← Loaded during planning
    ├── modules.md           ← Loaded during planning + execution
    ├── conventions.md       ← Loaded during execution
    ├── dependencies.md      ← Loaded on demand
    └── knowledge-graph.md   ← Loaded for complex tasks
```

### Hierarchical Loading

Not all memory is loaded every time. The agent selects what it needs:

| Context | What's Loaded |
|---------|--------------|
| **Always** | `memory.md` — tech stack, structure, state, module registry |
| **Planning** | + `architecture.md` + relevant sections of `modules.md` |
| **Execution** | + `conventions.md` + `modules.md` + `knowledge-graph.md` |
| **On demand** | `dependencies.md` when adding/changing packages |

### Indexing Pipeline

When memory is built or updated, it runs 7 phases:

1. **Structure** — File tree scan, folder→purpose mapping
2. **Config** — Extract from `package.json`, `tsconfig`, `docker-compose`, etc.
3. **Parsing** — Functions, classes, interfaces via source analysis
4. **Resolution** — Import chains, call graphs, inheritance
5. **Clustering** — Group symbols into functional communities
6. **Process Tracing** — Execution flows from entry points
7. **Compression** — Remove redundancy, maximize density

### Update Rules

- Memory updates **only when you ask** (`update memory`) or when a new task starts.
- Updates are **incremental** — only changed sections are modified.
- Token budget: ~2000 tokens max per update operation.
- Rolling summary when a file exceeds ~300 lines.
- Domain separation: frontend, backend, DB, infra never mixed in the same file.

---

## 🔌 CLI Compatibility

| CLI | Instruction File | How It Works |
|-----|-------------------|-------------|
| **Claude Code** | `AGENTS.md` → `CODER.md` | Claude Code auto-reads `AGENTS.md` which points to the full agent |
| **Gemini CLI** | `GEMINI.md` → `CODER.md` | Gemini auto-reads `GEMINI.md` which points to the full agent |
| **Codex CLI** | `AGENTS.md` → `CODER.md` | Codex auto-reads `AGENTS.md` which points to the full agent |
| **Other** | Load `CODER.md` manually | Any agent that can read a system prompt file will work |

The agent brain lives in `CODER.md`. The other files (`AGENTS.md`, `GEMINI.md`) are thin bridges that tell each CLI to read it.

---

## 📁 Repository Structure

```
.
├── CODER.md                              # Agent instructions (source of truth)
├── AGENTS.md                                # Bridge for Claude Code / Codex CLI
├── GEMINI.md                                # Bridge for Gemini CLI
├── .claude/
│   └── settings.json                        # Permissions for Claude Code
├── coder-factory/
│   ├── coder-memory/
│   │   ├── memory.md                        # Main memory index
│   │   ├── architecture.md                  # Architecture & patterns
│   │   ├── modules.md                       # Module map
│   │   ├── conventions.md                   # Code style rules
│   │   ├── dependencies.md                  # Packages & scripts
│   │   └── knowledge-graph.md               # Symbol graph & call chains
│   ├── coder-board/
│   │   └── coder-board.md                   # Kanban board (Obsidian plugin compatible)
│   └── coder-notes/                         # Task notes (auto-created)
├── templates/
│   └── TAREA-TEMPLATE.md                    # Task note template
└── README.md                                # This file
```

---

## 🎯 Obsidian Integration

The Kanban board (`coder-board.md`) is compatible (optional) with the [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban):

1. Open Obsidian → Settings → Community Plugins → Browse
2. Search **Kanban** → Install → Enable
3. Open `coder-board.md` — it renders as a visual board

Task notes in `coder-notes/` are regular Obsidian notes with full linking, search, and graph view support.

---

## 📝 Versioning

The agent follows semantic versioning: `v0.YYYYMMDDHHMM`

- `0` — Major version (pre-1.0, expect breaking changes)
- `YYYYMMDDHHMM` — Timestamp of the release

Current version: **v0.202604112034**

---

## 🤝 Contributing

1. Fork the repo.
2. Create a branch: `git checkout -b feature/your-feature`
3. Edit `CODER.md` (single source of truth for agent behavior).
4. Update version timestamp.
5. Submit a PR with a clear description of changes.

---

## 📄 License

MIT — use it, fork it, build on it.

---

<p align="center">
  <sub>Jose Antonio Lopez - Built with obsessive attention to token efficiency.</sub>
</p>
