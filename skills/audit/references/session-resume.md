# Audit — Session resume

This document is loaded on-demand — only when a `.minottobot/` directory is found at session init (see "Session init" in [SKILL.md](../SKILL.md)). It governs how the Audit skill greets a returning engagement and hands the previous snapshot forward.

For snapshot writing and the delta view appended to the final report, see [snapshot-delta.md](../../strategy/references/snapshot-delta.md) (Strategy skill) — that half runs after the plan exists, not here.

---

## Session types

**Fresh audit** — no `.minottobot/` directory found at session start. Run the full Audit workflow (Recon → Phase 0 → Phase 1) as normal. No greeting needed.

**Returning engagement** — a `.minottobot/audit-YYYY-MM-DD.md` file was found at session start. Open the session with the returning engagement summary below, then run the full Audit workflow as normal.

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
