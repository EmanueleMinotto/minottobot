# minottobot — Persistence

This document is loaded at Phase 2, when producing the final report. It governs how minottobot handles multi-session engagements: saving audit snapshots, loading previous audits, and generating delta views.

---

## Session types

**Fresh audit** — no `.minottobot/` directory found at session start. Run the full workflow (Recon → Phase 0 → Phase 1 → Phase 2). At the end, produce a snapshot file.

**Returning engagement** — a `.minottobot/audit-YYYY-MM-DD.md` file was found at session start. Open the session with a returning engagement summary, run the full workflow, then append a delta view to the final report.

---

## Returning engagement opening

When a previous audit snapshot was loaded at session start, open the conversation with:

```
Welcome back. Last audit: {date}, {team}.

Repos previously in scope: {list}

Last scores:
| Area | Score |
|------|-------|
| CI/CD | ?/5 |
| Testing | ?/5 |
| Code review | ?/5 |
| Monitoring | ?/5 |
| Developer Experience | ?/5 |
| Ownership & culture | ?/5 |

Last top 3 blockers:
1. ...
2. ...
3. ...

What has changed since then? (new repos, tech changes, remediation done, team changes?)
```

Then proceed with Code Reconnaissance and Phase 0 as normal. The previous audit informs Phase 1 context and the Phase 2 delta view — it does not replace fresh data collection.

---

## Snapshot file format

At the end of every audit, produce the snapshot block below and tell the user:

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
3. ...

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

When a previous audit exists, append a delta section **after** the standard required report format. Do not replace or shorten any part of the standard report.

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
