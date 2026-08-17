# Strategy — Snapshot & delta

This document is loaded on-demand — only when a previous audit was carried forward from the Audit skill (returning engagement), or when file-write tools are available. It governs how the Strategy skill saves progress snapshots and generates delta views once the improvement plan exists.

For how a returning engagement is detected and greeted at session start, see [session-resume.md](../../audit/references/session-resume.md) (Audit skill) — that half runs before the audit even starts, not here.

---

## Snapshot file format

At the end of every engagement, produce the snapshot block and handle it based on tool availability:

**If file-write tools are available (Write, Bash):** write the snapshot to `.minottobot/audit-{date}.md` in the workspace root, then confirm to the user where it was saved.

**If file-write tools are not available:** output the snapshot block as-is and tell the user:

> **Save this as `.minottobot/audit-{date}.md`** in your workspace root to enable progress tracking in future sessions.

```markdown
---
format_version: 1
date: YYYY-MM-DD
team: "{team name}"
repos:
  - name: "{repo name}"
    tech: "{primary tech}"
---

# minottobot audit snapshot — {team} — {date}

## Repos in scope
- {repo name} ({primary tech})

## Area scores
| Area | Score |
|------|-------|
| CI/CD | ? |
| Testing | ? |
| Code review | ? |
| Monitoring | ? |
| Developer Experience | ? |
| Ownership & culture | ? |

## Top 3 blockers
1. ...
2. ...

## Action items
| ID | Description | Horizon | Owner | Status |
|----|-------------|---------|-------|--------|
| A1 | ... | short | | open |
| A2 | ... | medium | | open |
```

**Action item ID rules:**
- IDs are stable identifiers across sessions: `A1`, `A2`, `A3`, ...
- Never reuse an ID that appeared in a previous session's snapshot.
- New items in a returning engagement continue from the highest previous ID (e.g., if the last session had A1–A5, new items start at A6).

---

## Delta view

When the audit output handed off by the Audit skill originated from a returning engagement, append a delta section **after** the standard required report format. Do not replace or shorten any part of the standard report.

```markdown
## Delta since {previous date}

### Score changes
| Area | Previous | Current | Change |
|------|----------|---------|--------|
| 🟡 CI/CD | 2/5 | 3/5 | ↑ +1 |
| 🔴 Testing | 1/5 | 1/5 | — |
| 🟢 Code review | 3/5 | 4/5 | ↑ +1 |
| 🟡 Monitoring | 2/5 | 2/5 | — |
| 🟡 Developer Experience | 2/5 | 3/5 | ↑ +1 |
| 🟡 Ownership & culture | 3/5 | 3/5 | — |

> Emoji reflects the **current** score: 🔴 1–2 · 🟡 3 · 🟢 4–5

### Blockers
- **Resolved:** ...
- **Still open:** ...
- **New:** ...

### Action items
| ID | Description | Status change |
|----|-------------|---------------|
| A1 | ... | ○ open → ✓ done |
| A2 | ... | still open |
| A3 | ... | new |

### Repo scope
- Added: {repo name} ({tech}) — no previous data to compare
- Removed: {repo name} — dropped from scope
```

**Delta rules:**
- Use `—` (not `0` or `+0`) when a score did not change.
- Use `↑ +N` / `↓ -N` for score changes.
- If a repo is new this session, note it as "added — no previous data to compare."
- If a repo was in the previous audit but is absent this session, note it as "dropped from scope" and do not carry forward its findings.
- The delta is appended to the report, never substituted for any part of it.
