<p align="center">
  <img src="https://img.shields.io/badge/version-0.202604141134-blue?style=flat-square" alt="version" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license" />
  <img src="https://img.shields.io/badge/format-Markdown-orange?style=flat-square" alt="markdown" />
</p>

<h1 align="center">🤖 Coder Agent</h1>

<p align="center">
  <strong>The AI coding agent that actually knows what it's doing. Persistent memory. Human-in-the-loop. Full lifecycle.</strong><br/>
  Kanban workflow · AI-optimized memory · Knowledge graph · Works with any LLM CLI.
</p>

```text
░█████╗  █████╗ ██████╗ ███████╗██████╗    █████╗  ██████╗ ███████╗███╗  ██╗████████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗  ██╔══██╗██╔════╝ ██╔════╝████╗ ██║╚══██╔══╝
██║  ╚═╝██║  ██║██║  ██║█████╗  ██████╔╝  ███████║██║  ██╗ █████╗  ██╔██╗██║   ██║
██║  ██╗██║  ██║██║  ██║██╔══╝  ██╔══██╗  ██╔══██║██║  ╚██╗██╔══╝  ██║╚████║   ██║
╚█████╔╝╚█████╔╝██████╔╝███████╗██║  ██║  ██║  ██║╚██████╔╝███████╗██║ ╚███║   ██║
 ╚════╝  ╚════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚══╝   ╚═╝
```

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

Coder is an **agent instruction set** that turns any LLM CLI into a disciplined software developer. It operates through Markdown files following a strict Kanban workflow with human-in-the-loop review cycles.

**The key idea:** Coder doesn't just write code. It builds and maintains an AI-optimized context memory across your entire project: knowledge graphs, architectural decisions, technology stack, feature connections, and system relationships — all compacted into versioned Markdown notes designed for maximum LLM comprehension.

### Why Coder?

- **Zero infrastructure** — No servers, no databases. Just Markdown files and your LLM CLI.
- **Human-in-the-loop** — Every plan goes through review before code is written.
- **Full traceability** — Every decision, change, and iteration is versioned with timestamps.
- **AI-optimized memory** — Knowledge graph with hierarchical loading, semantic compression, and domain separation. Designed for LLM consumption, not human reading.
- **Smart bug detection** — Coder identifies if a report is a bug on an existing task or a new task.
- **CLI-agnostic** — Works with Claude Code, Gemini CLI, Codex CLI, or any agent that reads instruction files.

---

## 🚀 Quick Start – run inside your project directory

### 1. Clone and copy

```bash
git clone https://github.com/jalopezsuarez/coder-agent.git
```

### 2. Launch your CLI

```bash
claude    # or gemini / codex
```

### 3. Initialize Coder and set the factory path

```bash
run coder-agent/src/AGENTS.md
```

Coder auto-creates the full `coder-factory/` structure and indexes your project into memory on first run.

### 4. Start working

```
> Coder create task Implement user authentication
> Coder plan
> Coder execute
> Coder status
```

### Recommendations

**Use the `coder-agent` folder as the `coder-factory` path** — When Coder asks for the factory path, point it to the same `coder-agent` directory. This keeps all Coder artifacts (`coder-factory/`, notes, board, memory) contained inside the gitignored folder, keeping your project tree clean.

  ```
  Human, where should I create or find coder-factory?                                                                                                           
  Give me the full path (it can be different from the current project).                                                                                       
  I cannot start working without this path.

  > ./coder-agent
  ```

**Add `coder-agent` to your `.gitignore`** — The cloned repository and all generated artifacts should not be committed to your project.

  ```bash
  echo "coder-agent" >> .gitignore
  ```  

---

## 🖥️ Kanban Board Manager Service

A self-contained Kanban board manager at `coder-factory/kanban.py`. Zero external dependencies — pure Python 3.

**Basic start service**
```bash
python3 kanban.py
```

**Advanced start service** *(kill existing process + restart in background)*
```bash
pkill -f "kanban.py"; sleep 1 && python3 kanban.py 2>&1 &
```

The service starts at `http://localhost:8089`.

**Board & Cards:**
- GitHub-dark themed Kanban board with all 6 color-coded columns (BACKLOG, PLAN, REVIEW, EXECUTION, TESTING, DONE)
- Cards display inline task ID badge (blue/white), title, summary, short date (d/m/yy HH:MM), and color-coded tags (#coder, #canceled)
- Drag & drop cards between columns — auto-saves board and updates task status and timestamp

**Live Reload (SSE):**
- File watcher thread monitors `coder-board.md` and `coder-tasks/` via `mtime` (zero polling, zero disk reads when idle)
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
- Tables, internal anchor links, external links, and Obsidian wiki-links (`[[C1 Title]]`)

**Extras:**
- Help modal with all Coder commands, workflow visualization, and tag reference
- REST API (`/api/board`, `/api/note`, `/api/events`) for board state, notes, and live events
- `ThreadingHTTPServer` for concurrent SSE streams and HTTP requests
- Responsive layout — sidebar goes full-width on mobile
- Keyboard shortcuts: Escape to close, Ctrl+S / Cmd+S to save, `/` to search

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
  │  move task to PLAN           │                              │
  │                              │                              │
  │  "Coder plan"                │                              │
  │─────────────────────────────>│                              │
  │                              │──── process HUMAN-ONLY ────> │
  │                              │──── write PLANNING #1 ─────> │
  │                              │──── move to REVIEW ────────> │
  │                              │                              │
  │  review + write HUMAN-ONLY   │                              │
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
  │                              │──── identify task ─────────> │
  │                              │──── FIXES #1 ──────────────> │
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

All commands **require** the word **"Coder"** (or **"coder"**) in your message to activate the agent. Without it, the agent is bypassed and the LLM executes your request directly as a normal assistant. Coder can only work on tasks tagged `#coder` — tasks without it are human-owned. Tasks tagged `#canceled` are always skipped.

| Command | Description |
|---------|-------------|
| `Coder create task <desc>` | Create a task in BACKLOG with note |
| `Coder plan` | Plan eligible tasks in PLAN column |
| `Coder execute` | Implement eligible tasks in EXECUTION column |
| `Coder add to C1 <text>` | Append text to task's HUMAN-ONLY ZONE |
| `Coder status` | Show board summary |
| `Coder update memory` | Re-index project knowledge base |
| `Coder for C5 <instruction>` | Add instruction to specific task |
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

Human, this looks like a bug on C25 "Implement sidebar navigation".
Should I add a FIXES entry there?
```

If the matched task is missing `#coder` or has `#canceled`, Coder informs you it cannot work on it. If it can't identify the task, it asks. If it's clearly new, it suggests creating a task. **Nothing goes untracked.**

---

## 📝 Task Notes

Every task gets a dedicated note in `coder-tasks/` with this structure:

```
┌──────────────────────────────────┐
│ # C1 Implement user auth         │
│ > Status | Created | Updated     │
├──────────────────────────────────┤
│ SUMMARY              ← Coder     │  Last action snapshot (overwritten).
├──────────────────────────────────┤
│ TABLE OF CONTENTS    ← Auto      │  Clickable navigation index.
├──────────────────────────────────┤
│ INSTRUCTIONS         ← Human     │  HUMAN-ONLY ZONE + processed
│   HUMAN-ONLY ZONE   ← writes     │  iterations. You write here,
│   INSTRUCTIONS #1..N ← Processed │  Coder processes and restores.
├──────────────────────────────────┤
│ PLANNING #1..N       ← Coder     │  Versioned plans.
├──────────────────────────────────┤
│ EXECUTION #1..N      ← Coder     │  Versioned implementations.
├──────────────────────────────────┤
│ FIXES #1..N          ← Coder     │  Versioned fixes.
└──────────────────────────────────┘
```

### SUMMARY

The `SUMMARY` section always reflects the **last action** performed on the task. After every iteration (INSTRUCTIONS, PLANNING, EXECUTION, or FIXES), Coder **overwrites** SUMMARY with a matching entry: `### SUMMARY - PLANNING #1` + brief description. This gives an instant snapshot of where the task stands.

### HUMAN-ONLY ZONE Flow

1. Human writes in HUMAN-ONLY ZONE inside INSTRUCTIONS — replacing the placeholder code block (manually or via `Coder for C5 ...`).
2. On next state change, Coder processes it into `INSTRUCTIONS #(N+1)` with `> Created: YYYY-MM-DD HH:MM`.
3. HUMAN-ONLY ZONE is cleared and the placeholder code block is restored:
   ````
   ```
   Write your instructions here.
   Coder will process this into INSTRUCTIONS and clear it on next state change.
   ```
   ````
4. SUMMARY and TABLE OF CONTENTS are updated.

### Key Design Decisions

- **Filenames match titles** — `C1 Implement user authentication.md` links directly from the Kanban board via `[[C1 Implement user authentication]]`.
- **Titles are clean** — No symbols, no tech dumps. Just a clear summary: "Implement user authentication", not "JS+JWT+Fastify auth module".
- **Tasks use C<N> IDs** — simple incremental numbering (C1, C2, C3...) for clear tracking.
- **Strict section containment** — Each iteration type goes ONLY in its matching section (INSTRUCTIONS under `## INSTRUCTIONS`, PLANNING under `## PLANNING`, etc.). Never mixed.
- **Newest first** — Iterations within each section are ordered most recent at the top, oldest at the bottom (#3, #2, #1).
- **Clean headings, timestamp below** — Headings use `### PLANNING #1` (no timestamp), with `> Created: YYYY-MM-DD HH:MM` on the next line. This produces simple anchor IDs (`#planning-1`) that work in Obsidian and all Markdown renderers.
- **Notes are incremental** — PLANNING #1 is never modified; #2 is added above it. All content preserved in full.

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
└── coder-tasks/                                # Task notes (auto-created)
```

---

## 🎯 Obsidian Integration (optional)

### Kanban Plugin

The board uses the [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban):

1. Settings → Community Plugins → Browse → **Kanban** → Install → Enable
2. Open `coder-board.md` — renders as a visual board
3. Tasks auto-link: `[[C1 Implement user authentication]]` opens the note directly

### Settings

The board includes Kanban settings that auto-create new notes in the `coder-tasks/` folder:

```
%% kanban:settings
{"kanban-plugin":"board","new-note-folder":"coder-tasks"}
%%
```

---

## 📝 Versioning

Format: `v0.YYYYMMDDHHMM`

- `0` — Major version (pre-1.0)
- `YYYYMMDDHHMM` — Release timestamp

Current: **v0.202604141134**

---

## 🤝 Contributing

1. Fork the repo
2. `git checkout -b feature/your-feature`
3. Edit `CODER.md` (single source of truth)
4. Update version timestamp
5. Submit PR

---

## 📄 License

MIT License - Copyright (c) 2026 Jose Antonio López

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

<p align="center">
  <sub>Built for developers who want AI coding assistants that follow process, not chaos.</sub>
</p>
