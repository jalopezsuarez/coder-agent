<p align="center">
  <img src="https://img.shields.io/badge/version-0.202604122200-blue?style=flat-square" alt="version" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license" />
  <img src="https://img.shields.io/badge/format-Markdown-orange?style=flat-square" alt="markdown" />
</p>

<h1 align="center">🤖 Coder Agent</h1>

<p align="center">
  <strong>The AI coding agent that actually knows what it's doing. Persistent memory. Human-in-the-loop. Full lifecycle.</strong><br/>
  Kanban workflow · AI-optimized memory · Knowledge graph · Works with any LLM CLI.
</p>

<p align="center">
  <img src="coder-agent.png" alt="Coder Agent" width="400"/>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-memory-system">Memory System</a> •
  <a href="#-task-notes">Task Notes</a> •
  <a href="#-cli-compatibility">CLI Compatibility</a>
</p>

---

## What is Coder?

Coder is an **agent instruction set** that turns any LLM CLI into a disciplined software developer. It operates through Markdown files — compatible with the Obsidian Kanban plugin, but fully usable standalone — following a strict Kanban workflow with human-in-the-loop review cycles.

**The key idea:** Coder doesn't just write code. It builds and maintains an AI-optimized context memory across your entire project: knowledge graphs, architectural decisions, technology stack, feature connections, and system relationships — all compacted into versioned Markdown notes designed for maximum LLM comprehension.

### Why Coder?

- **Zero infrastructure** — No servers, no databases. Just Markdown files and your LLM CLI.
- **Human-in-the-loop** — Every plan goes through review before code is written.
- **Full traceability** — Every decision, change, and iteration is versioned with timestamps.
- **AI-optimized memory** — Knowledge graph with hierarchical loading, semantic compression, and domain separation. Designed for LLM consumption, not human reading.
- **Smart bug detection** — Coder identifies if a report is a bug on an existing task or a new task.
- **CLI-agnostic** — Works with Claude Code, Gemini CLI, Codex CLI, or any agent that reads instruction files.

---

## 🚀 Quick Start

### 1. Clone and copy

```bash
cd /path/to/your/project/
git clone https://github.com/jalopezsuarez/coder-agent.git
```
```bash
cp coder-agent/src/{CODER.md,AGENTS.md,GEMINI.md} .
cp -r coder-agent/.claude .
```

### 2. Launch your CLI

```bash
claude    # or gemini / codex
```

### 3. Coder asks for the factory path

```
Human, where should I create or find coder-factory?
Give me the full path. I cannot start working without it.
```

### 4. Start working

```
> Coder create task Implement user authentication
> Coder plan
> Coder execute
> Coder status
```

Coder auto-creates the full `coder-factory/` structure and indexes your project into memory on first run.

### Recommendations

- **Use the `coder-agent` folder as the `coder-factory` path** — When Coder asks for the factory path, point it to the same `coder-agent` directory. This keeps all Coder artifacts (`coder-factory/`, notes, board, memory) contained inside the gitignored folder, keeping your project tree clean.

  ```
  Human, where should I create or find coder-factory?
  > ./coder-agent
  ```

- **Add `coder-agent` to your `.gitignore`** — The cloned repository and all generated artifacts should not be committed to your project.

  ```bash
  echo "coder-agent" >> /path/to/your/project/.gitignore
  ```

---

## 🔄 How It Works

```
 Human                        Coder                         Project
  │                              │                              │
  │  "Coder create task X"       │                              │
  │─────────────────────────────>│                              │
  │                              │──── create note ───────────> │
  │                              │──── add to BACKLOG ────────> │
  │                              │                              │
  │  move task to PLAN          │                              │
  │                              │                              │
  │  "Coder plan"                │                              │
  │─────────────────────────────>│                              │
  │                              │──── process USER PROMPT ───> │
  │                              │──── write PLANNING #1 ─────> │
  │                              │──── move to REVIEW ────────> │
  │                              │                              │
  │  review + write USER PROMPT  │                              │
  │  move to PLAN                │                              │
  │                              │                              │
  │  "Coder plan"                │                              │
  │─────────────────────────────>│                              │
  │                              │──── INSTRUCTIONS #1 ───────> │
  │                              │──── PLANNING #2 (delta) ───> │
  │                              │──── move to REVIEW ────────> │
  │                              │                              │
  │  approve → EXECUTION         │                              │
  │                              │                              │
  │  "Coder execute"             │                              │
  │─────────────────────────────>│                              │
  │                              │──── implement code ────────> │
  │                              │──── write EXECUTION #1 ────> │
  │                              │──── move to TESTING ───────> │
  │                              │                              │
  │  "sidebar doesn't collapse"  │                              │
  │─────────────────────────────>│                              │
  │                              │──── identify task ────────> │
  │                              │──── BUG FIX #1 ────────────> │
  │                              │                              │
  │  validate → DONE             │                              │
```

### Kanban Columns

| Column | Owner | Description |
|--------|-------|-------------|
| **BACKLOG** | Coder/Human | Tasks created, waiting to be prioritized |
| **PLAN** | Coder | Coder generates detailed plans |
| **REVIEW** | Human | Human reviews the plan, adds feedback |
| **EXECUTION** | Coder | Coder writes the actual code |
| **TESTING** | Human | Human validates the implementation |
| **DONE** | Human | Task completed |

---

## ⚡ Commands

All commands require the **"Coder"** prefix to activate the agent. Coder can only work on tasks tagged `#coder` — tasks without it are human-owned. Tasks tagged `#canceled` are always skipped.

| Command | Description |
|---------|-------------|
| `Coder create task <desc>` | Create a task in BACKLOG with note |
| `Coder plan` | Plan eligible tasks in PLAN column |
| `Coder execute` | Implement eligible tasks in EXECUTION column |
| `Coder move T001 to PLAN` | Move task between columns |
| `Coder add to T001 <text>` | Append text to task's USER PROMPT |
| `Coder status` | Show board summary |
| `Coder update memory` | Re-index project knowledge base |
| `Coder for T005 <instruction>` | Add instruction to specific task |
| `Coder <bug description>` | Smart detection: bug or new task? |

### Tags

| Tag | Effect |
|-----|--------|
| `#coder` | **Required** — Task assigned to the agent. Without this tag, Coder cannot plan, execute, move, or modify the task |
| `#canceled` | Task canceled — Coder skips it entirely, only human can toggle |

### Smart Bug Detection

When you report an issue, Coder tries to match it to an existing task (only those with `#coder` and without `#canceled`):

```
> Coder the sidebar doesn't collapse on mobile

Human, this looks like a bug on T025 "Implement sidebar navigation".
Should I add a BUG FIX entry there?
```

If the matched task is missing `#coder` or has `#canceled`, Coder informs you it cannot work on it. If it can't identify the task, it asks. If it's clearly new, it suggests creating a task. **Nothing goes untracked.**

---

## 📝 Task Notes

Every task gets a dedicated note in `coder-notes/` with this structure:

```
┌──────────────────────────────────┐
│ # T001 Implement user auth       │
│ > Status | Created | Updated     │
├──────────────────────────────────┤
│ USER PROMPT          ← Human     │  You write here. Coder processes
│                      writes      │  it and clears it on state change.
├──────────────────────────────────┤
│ TABLE OF CONTENTS    ← Auto      │  Clickable navigation index.
├──────────────────────────────────┤
│ INSTRUCTIONS #1..N   ← Processed │  Processed from USER PROMPT.
├──────────────────────────────────┤
│ PLANNING #1..N       ← Coder     │  Versioned plans.
├──────────────────────────────────┤
│ EXECUTION #1..N      ← Coder     │  Versioned implementations.
├──────────────────────────────────┤
│ BUG FIX #1..N        ← Coder     │  Versioned bug fixes.
└──────────────────────────────────┘
```

### USER PROMPT Flow

1. Human writes in USER PROMPT (manually or via `Coder for T005 ...`).
2. On next state change, Coder processes it into `INSTRUCTIONS #(N+1)`.
3. USER PROMPT is cleared.
4. Table of contents is updated.

### Key Design Decisions

- **Filenames match titles** — `T001 Implement user authentication.md` links directly from the Kanban board via `[[T001 Implement user authentication]]`.
- **Titles are clean** — No symbols, no tech dumps. Just a clear summary: "Implement user authentication", not "JS+JWT+Fastify auth module".
- **Tasks use T### IDs** — correlative numbering (T001, T002, T003...) for clear tracking.
- **All sections are append-only** — PLANNING #1 is never modified; #2 is appended with the delta.

---

## 🧠 Memory System

Coder maintains an AI-optimized knowledge base with hierarchical loading and semantic compression.

### Architecture

```
coder-factory/coder-memory/
├── memory.md            ← Always loaded (~50-100 lines)
├── architecture.md      ← Loaded during planning
├── modules.md           ← Loaded during planning + execution
├── conventions.md       ← Loaded during execution
├── dependencies.md      ← Loaded on demand
└── knowledge-graph.md   ← Loaded for complex tasks
```

### Knowledge Graph

The memory includes a codebase knowledge graph built through a multi-phase pipeline:

1. **Structure** — File tree scan, folder→purpose mapping
2. **Config** — Extract from manifests (package.json, tsconfig, etc.)
3. **Parsing** — Functions, classes, interfaces extraction
4. **Resolution** — Import chains, call graphs, inheritance
5. **Clustering** — Group symbols into functional communities
6. **Process Tracing** — Execution flows from entry points
7. **Compression** — Remove redundancy, maximize information density

### Update Policy

- **Manual only** — Memory updates only when you say `Coder update memory`.
- Coder **reminds** you to update before and after executions.
- Updates are incremental (~2000 token budget per update).
- All timestamps use `YYYY-MM-DD HH:MM` format.

---

## 🔌 CLI Compatibility

| CLI | Instruction File | Startup |
|-----|-------------------|---------|
| **Claude Code** | `AGENTS.md` → `CODER.md` | `claude` |
| **Gemini CLI** | `GEMINI.md` → `CODER.md` | `gemini` |
| **Codex CLI** | `AGENTS.md` → `CODER.md` | `codex` |
| **Other** | Load `CODER.md` directly | — |

The agent brain lives in `CODER.md`. Bridge files (`AGENTS.md`, `GEMINI.md`) tell each CLI to read it.

---

## 📁 Repository Structure

```
.
├── README.md                                   # Project overview (this file)
├── CLAUDE.md                                   # Instructions for Claude Code
├── coder-agent.png                             # Project banner
├── .claude/                                    # Claude Code settings
└── src/                                        # Source files (copy to your project)
    ├── CODER.md                                # Agent brain (source of truth)
    ├── AGENTS.md                               # Bridge: Claude Code / Codex CLI
    ├── GEMINI.md                               # Bridge: Gemini CLI
    ├── kanban.py                               # Kanban board manager (python3 kanban.py)
    ├── task-template.md                       # Task note template
    ├── coder-board.md                          # Kanban board template
    ├── memory.md                               # Main memory index template
    ├── architecture.md                         # Architecture & patterns template
    ├── modules.md                              # Module map template
    ├── conventions.md                          # Code conventions template
    ├── dependencies.md                         # Dependencies template
    └── knowledge-graph.md                      # Knowledge graph template
```

At runtime, Coder auto-generates the `coder-factory/` structure in your project:

```
<CODER_FACTORY_ROOT>/coder-factory/
├── kanban.py                                   # Kanban board manager (copied from src/)
├── coder-memory/                               # AI-optimized knowledge base
│   ├── memory.md                               # Main index (always loaded)
│   ├── architecture.md                         # Architecture & patterns
│   ├── modules.md                              # Module map
│   ├── conventions.md                          # Code style
│   ├── dependencies.md                         # Packages & scripts
│   └── knowledge-graph.md                      # Symbol graph & call chains
├── coder-board/
│   └── coder-board.md                          # Kanban board
└── coder-notes/                                # Task notes (auto-created)
```

---

## 🖥️ Kanban Board Manager

A self-contained Kanban board manager at `coder-factory/kanban.py`. Zero external dependencies — pure Python 3.

```bash
cd coder-factory
python3 kanban.py
```

The server starts at `http://localhost:8089`.

**Board & Cards:**
- GitHub-dark themed Kanban board with all 6 color-coded columns (BACKLOG, PLAN, REVIEW, EXECUTION, TESTING, DONE)
- Cards display inline task ID badge (blue/white), title, content preview, short date (d/m/yy HH:MM), and color-coded tags (#coder, #canceled)
- Drag & drop cards between columns — auto-saves board and updates task status and timestamp

**Live Reload (SSE):**
- File watcher thread monitors `coder-board.md` and `coder-notes/` via `mtime` (zero polling, zero disk reads when idle)
- Server-Sent Events push changes to the browser — board updates automatically within ~1 second
- Single persistent connection with automatic reconnection — no repeated HTTP requests

**Search & Filter:**
- Real-time search input in the toolbar — filters cards as you type
- Accent and case insensitive (e.g., "informacion" matches "Información")
- Keyboard shortcut: press `/` to focus the search box
- Column counts update to reflect visible cards

**Task Sidebar:**
- Click any card to open a sidebar with the full task note
- Three view modes: **Edit** (WYSIWYG), **Source** (raw Markdown), and **View** (read-only rendered)
- Tag toggle buttons (`#coder`, `#canceled`) — click to toggle, persisted on save
- Save changes with Ctrl+S / Cmd+S — scroll position preserved between mode switches

**Built-in Markdown Renderer:**
- Headers, bold, italic, strikethrough, inline code, code blocks, blockquotes
- Ordered, unordered, and nested lists with task list support (checkboxes)
- Tables, internal anchor links, external links, and Obsidian wiki-links (`[[T001 Title]]`)

**Extras:**
- Help modal with all Coder commands, workflow visualization, and tag reference
- REST API (`/api/board`, `/api/note`, `/api/events`) for board state, notes, and live events
- `ThreadingHTTPServer` for concurrent SSE streams and HTTP requests
- Responsive layout — sidebar goes full-width on mobile
- Keyboard shortcuts: Escape to close, Ctrl+S / Cmd+S to save, `/` to search
- Obsidian Kanban plugin compatible — preserves board settings

---

## 🎯 Obsidian Integration (optional)

### Kanban Plugin

The board uses the [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban):

1. Settings → Community Plugins → Browse → **Kanban** → Install → Enable
2. Open `coder-board.md` — renders as a visual board
3. Tasks auto-link: `[[T001 Implement user authentication]]` opens the note directly

### Settings

The board includes Kanban settings that auto-create new notes in the `coder-notes/` folder:

```
%% kanban:settings
{"kanban-plugin":"board","new-note-folder":"coder-notes"}
%%
```

---

## 📝 Versioning

Format: `v0.YYYYMMDDHHMM`

- `0` — Major version (pre-1.0)
- `YYYYMMDDHHMM` — Release timestamp

Current: **v0.202604122200**

---

## 🤝 Contributing

1. Fork the repo
2. `git checkout -b feature/your-feature`
3. Edit `CODER.md` (single source of truth)
4. Update version timestamp
5. Submit PR

---

## 📄 License

MIT

---

<p align="center">
  <sub>Built for developers who want AI coding assistants that follow process, not chaos.</sub>
</p>
