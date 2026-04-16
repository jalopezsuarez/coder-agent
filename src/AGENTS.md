# Coder Agent

Read and strictly follow all instructions in `CODER.md` in this same directory.
That file is the single source of truth for agent behavior, memory system, and workflow.

## Quick Command Reference

- `Coder create task <description>` — Create task in BACKLOG with DEFINE #1.
- `Coder define <question>` — Business consultation on a task (expert, non-technical).
- `Coder plan` — Plan tasks in PLAN column.
- `Coder execute` — Implement tasks in EXECUTION column.
- `Coder status` — Summarize Kanban board.
- `Coder update memory` — Re-index project knowledge base.
- `Coder for C<N> <instruction>` — Add functional definition to specific task.
- `Coder add to C<N> <text>` — Append text to task's HUMAN-ONLY ZONE.
- `Coder <bug description>` — Smart detection: bug on existing task or new task.
