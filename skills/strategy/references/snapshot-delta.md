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
- New items in a returning engagement continue from the highest previous ID (e.g., if the last session had A1–A5, new items start at A6). On a returning engagement the Audit skill already carried forward `next_action_id` — start there rather than recounting.

After writing the snapshot file, check it if Bash and `python3` are available:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/snapshot.py" validate .minottobot/audit-{date}.md
```

Do the same for the improvement plan itself, which the script recognises as a `report`. Exit 1 lists what to fix; exit 2 means the script could not run, so verify by hand instead of blocking.

---

## Delta view

When the audit output handed off by the Audit skill originated from a returning engagement, append a delta section **after** the standard required report format. Do not replace or shorten any part of the standard report.

**Generate it with the script, not by hand.** Once the new snapshot file is written, the delta is pure arithmetic over two files:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/snapshot.py" delta \
  .minottobot/audit-{previous date}.md .minottobot/audit-{date}.md
```

Append its output verbatim — it already applies every rule below. Two caveats: blockers are prose, so the script pairs them by text similarity and can misfile a blocker that was reworded beyond recognition; read the Blockers section it produced and correct it if a pairing is wrong. And if the script is unavailable, build the delta by hand to the same format.

The format it emits, and the format to produce by hand if the script cannot run:

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
- An action item present in the previous snapshot but absent from this one is `dropped from plan` — do not silently omit its row.
- If a repo is new this session, note it as "added — no previous data to compare."
- If a repo was in the previous audit but is absent this session, note it as "dropped from scope" and do not carry forward its findings.
- The delta is appended to the report, never substituted for any part of it.
