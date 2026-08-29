# Audit — Session resume

This document is loaded on-demand — only when a `.minottobot/` directory is found at session init (see "Session init" in [SKILL.md](../SKILL.md)). It governs how the Audit skill greets a returning engagement and hands the previous snapshot forward.

For snapshot writing and the delta view appended to the final report, see [snapshot-delta.md](../../strategy/references/snapshot-delta.md) (Strategy skill) — that half runs after the plan exists, not here.

---

## Session types

**Fresh audit** — no `.minottobot/` directory found at session start. Run the full Audit workflow (Recon → Phase 0 → Phase 1) as normal. No greeting needed.

**Returning engagement** — a `.minottobot/audit-YYYY-MM-DD.md` file was found at session start. Open the session with the returning engagement summary below, then run the full Audit workflow as normal.

---

## Reading the snapshot

If Bash and `python3` are available, parse the snapshot with the helper script rather than reading the numbers off the page:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/snapshot.py" parse .minottobot/audit-YYYY-MM-DD.md
```

It returns JSON with `date`, `team`, `repos`, `scores`, `blockers`, `action_items`, and `next_action_id` — the first free action item ID, which is what the Strategy skill needs to continue numbering without reusing one. Use those values verbatim in the greeting below and in the carry-forward.

Warnings go to stderr: an unrecognised `format_version` means the snapshot was written by a newer version of the plugin and some fields may be missing — say so to the user rather than guessing. Exit code 2 means the file could not be parsed; fall back to reading it yourself and mention that the snapshot is malformed, since that is itself a finding.

If the script is unavailable, read the snapshot directly — and compute `next_action_id` as the highest `A{n}` in the previous snapshot plus one.

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

Then proceed with Code Reconnaissance and Phase 0 as normal. The previous audit informs the current findings and evidence — it does not replace fresh data collection.

Carry the loaded snapshot's date, team, repos, scores, and action item IDs forward into the audit output (see "What audit hands off to strategy" in [SKILL.md](../SKILL.md)), so the Strategy skill can build the delta view and continue action item numbering without re-reading the snapshot file itself.
