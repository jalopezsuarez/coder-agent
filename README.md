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
  <a href="#-story-notes">Story Notes</a> •
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
- **Smart bug detection** — Coder identifies if a report is a bug on an existing story or a new task.
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
  │  move story to PLAN          │                              │
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
  │                              │──── identify story ────────> │
  │                              │──── BUG FIX #1 ────────────> │
  │                              │                              │
  │  validate → DONE             │                              │
```

### Kanban Columns

| Column | Owner | Description |
|--------|-------|-------------|
| **BACKLOG** | Coder/Human | Stories created, waiting to be prioritized |
| **PLAN** | Coder | Coder generates detailed plans |
| **REVIEW** | Human | Human reviews the plan, adds feedback |
| **EXECUTION** | Coder | Coder writes the actual code |
| **TESTING** | Human | Human validates the implementation |
| **DONE** | Human | Story completed |

---

## ⚡ Commands

All commands require the **"Coder"** prefix to activate the agent.

| Command | Description |
|---------|-------------|
| `Coder create task <desc>` | Create a story in BACKLOG with note |
| `Coder create task urgent <desc>` | Same, with `#urgent` tag |
| `Coder plan` | Plan all stories in PLAN column |
| `Coder execute` | Implement all stories in EXECUTION column |
| `Coder move S001 to PLAN` | Move story between columns |
| `Coder add to S001 <text>` | Append text to story's USER PROMPT |
| `Coder status` | Show board summary |
| `Coder update memory` | Re-index project knowledge base |
| `Coder for S005 <instruction>` | Add instruction to specific story |
| `Coder <bug description>` | Smart detection: bug or new task? |

### Tags

| Tag | Effect |
|-----|--------|
| `#coder` | Story assigned to the agent |
| `#urgent` | Processed first |
| `#blocked` | Agent will not touch it |

### Smart Bug Detection

When you report an issue, Coder tries to match it to an existing story:

```
> Coder the sidebar doesn't collapse on mobile

Human, this looks like a bug on S025 "Implement sidebar navigation".
Should I add a BUG FIX entry there?
```

If it can't identify the story, it asks. If it's clearly new, it suggests creating a story. **Nothing goes untracked.**

---

## 📝 Story Notes

Every story gets a dedicated note in `coder-notes/` with this structure:

```
┌──────────────────────────────────┐
│ # S001 Implement user auth       │
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

1. Human writes in USER PROMPT (manually or via `Coder for S005 ...`).
2. On next state change, Coder processes it into `INSTRUCTIONS #(N+1)`.
3. USER PROMPT is cleared.
4. Table of contents is updated.

### Key Design Decisions

- **Filenames match titles** — `S001 Implement user authentication.md` links directly from the Kanban board via `[[S001 Implement user authentication]]`.
- **Titles are clean** — No symbols, no tech dumps. Just a clear summary: "Implement user authentication", not "JS+JWT+Fastify auth module".
- **Stories (S###)** instead of tasks — aligns with agile terminology.
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
    ├── story-template.md                       # Story note template
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
└── coder-notes/                                # Story notes (auto-created)
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
- Cards display title, content preview, created/updated dates, story ID badge, and color-coded tags (#coder, #urgent, #blocked)
- Drag & drop cards between columns — auto-saves board and updates story status and timestamp

**Story Sidebar:**
- Click any card to open a sidebar with the full story note
- Three view modes: **Edit** (WYSIWYG), **Source** (raw Markdown), and **View** (read-only rendered)
- Save changes with Ctrl+S / Cmd+S — scroll position preserved between mode switches

**Built-in Markdown Renderer:**
- Headers, bold, italic, strikethrough, inline code, code blocks, blockquotes
- Ordered, unordered, and nested lists with task list support (checkboxes)
- Tables, internal anchor links, external links, and Obsidian wiki-links (`[[S001 Title]]`)

**Extras:**
- Help modal with all Coder commands, workflow visualization, and tag reference
- REST API (`/api/board`, `/api/note`) for reading and saving board state and notes
- Responsive layout — sidebar goes full-width on mobile
- Keyboard shortcuts: Escape to close, Ctrl+S / Cmd+S to save
- Obsidian Kanban plugin compatible — preserves board settings

---

## 🎯 Obsidian Integration (optional)

### Kanban Plugin

The board uses the [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban):

1. Settings → Community Plugins → Browse → **Kanban** → Install → Enable
2. Open `coder-board.md` — renders as a visual board
3. Stories auto-link: `[[S001 Implement user authentication]]` opens the note directly

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
