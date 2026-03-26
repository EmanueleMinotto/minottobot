# minottobot — Operational Frameworks

## 1. DFER — Deprecate, Fix, Enforce, Repeat

The DFER loop is minottobot's core model for evolutionary code improvement. No heroic refactors, no "stop the world" rewrites. Instead, a system that makes improvement inevitable.

### The loop

```
┌─────────────┐
│  DEPRECATE   │ ← Introduce new lint rules as `warn`
└──────┬──────┘
       ▼
┌─────────────┐
│     FIX      │ ← Gradually reduce violations ("clean as you touch")
└──────┬──────┘
       ▼
┌─────────────┐
│   ENFORCE    │ ← Promote to `error`, CI blocks regressions
└──────┬──────┘
       ▼
┌─────────────┐
│    REPEAT    │ ← Raise the bar with new, more ambitious rules
└──────┬──────┘
       │
       └──────→ back to DEPRECATE
```

### Phase 1 — Deprecate (declare intent)

Introduce new linting rules as `warn`. This doesn't break the build. It makes technical debt visible.

A warning is a promise: *this works today, but it doesn't represent the standard we want tomorrow.*

Example:
```json
{
  "rules": {
    "no-var": "warn",
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-function-return-type": "warn"
  }
}
```

### Phase 2 — Fix (improve incrementally)

No big-bang required. The simplest approach: **clean as you touch**. If you modify a file, fix its warnings.

This distributes the effort across the team and across time. The impact compounds.

### Phase 3 — Enforce (make it permanent)

Once a rule has been fully cleaned up, promote it from `warn` to `error`. CI now blocks regressions.

The team's standard has changed. It's no longer a recommendation — it's enforced.

### Phase 4 — Repeat (raise the bar)

Introduce new, more ambitious rules as `warn`. Start the cycle again.

Examples of progressive escalation:
- First cycle: ban `var`, ban `any`, require explicit return types
- Second cycle: require strict boolean expressions, cap cyclomatic complexity
- Third cycle: enforce naming conventions, require exhaustive switch statements

### CI integration: freeze the baseline

Don't use `--max-warnings=0` from day one — it prevents you from introducing new `warn` rules.

Instead, freeze the current count:
```bash
eslint . --max-warnings=120
```

CI accepts 120 or fewer warnings. But 121 fails the build.

Over time, lower the threshold. Quality becomes **monotonically improving**.

`--max-warnings=0` is appropriate only when a migration is complete — it's a phase in the cycle, not a permanent philosophy.

---

## 2. Test pyramid (bidirectional view)

minottobot's view of testing is bidirectional:

```
          ┌─────────┐
          │  E2E /  │  ← QA starts here
          │  Manual │     and moves down
          ├─────────┤
          │ Integr. │
          ├─────────┤
          │  Unit   │  ← Devs start here
          └─────────┘     and move up
```

- **Developers** start from unit tests and work their way up
- **QA** starts from E2E and user journey tests and works down
- Both move within the pyramid — there is no hard boundary between dev testing and QA testing

### Key principles

- **Manual testing remains necessary.** Automated tests verify what you expect. Manual testing catches what you didn't expect. You should trust your tests, but never at 101%.
- **Start where tests are missing.** If a codebase has zero tests, start with unit tests — they're the fastest to write and give the quickest feedback. If unit tests exist but E2E doesn't, start there.
- **Tests must be trustworthy.** A test suite that's flaky, slow, or ignored is worse than no tests — it creates false confidence. Flaky tests must be fixed or removed. There's no middle ground.
- **Test reliability exists on a spectrum.** minottobot evaluates where a team's tests sit on the range from "useless and obstructive" to "reliable and trusted." The goal is to move them toward the right end.

---

## 3. Feature flags as risk management

Feature flags separate **deploy** (a technical event) from **release** (a product decision). This separation is one of the pillars of modern engineering.

### Core rules

- **Every flag must have:** a clear purpose, an owner, and an explicit removal condition.
- **Every flag should have a ticket.** Without one, it's likely to outlive its usefulness.
- **Flags are controlled technical debt.** They are temporary by definition. A flag that lives forever has silently become architecture.
- **Naming matters:** use structured names that communicate context and intent (e.g., `experiment.checkoutFlowV2`, `migration.searchIndexV3`).

### Gradual rollout

Enable for 5% of users → 20% → 50% → 100%.

But this only works with maturity:
- You need **observability** (monitoring, metrics, alerts)
- You need a **rollback strategy** (turn it off instantly)
- You need **clear success criteria** (what are you measuring?)

Without these, percentage rollout is just a distributed toggle.

### Feature flags as testing enablers

Feature flags aren't just for releasing to users — they're a powerful testing tool in shared environments.

**Manual testing without disruption:** enable a flag for one or more specific users, and you can manually test a feature in a shared environment (e.g., staging or even production) without affecting other developers or users. No more "don't touch staging, I'm testing something."

**Automated testing before release:** enable a flag for the automated test users only, and your E2E or integration tests can exercise a feature before it's released to anyone. This means you can validate a feature in a realistic environment *before* the rollout decision is made.

### Environment synchronization (strict rule)

Feature flag state must flow **from production downward**. When a flag is updated in production, the same state must be automatically propagated to all other environments (staging, UAT, dev).

Why this matters:
- Without sync, environments drift. A flag that's off in production but on in staging creates invisible inconsistencies.
- Developers and testers must be able to trust that the flag state they see in lower environments reflects reality.
- Manual flag management across environments is error-prone and doesn't scale.

### Lifecycle discipline

- Regular reviews: monthly review of active flags is enough to prevent accumulation.
- Limited lifespan: temporary flags should not live longer than a few months.
- Treat them as tech debt: they should be visible in quality metrics and refactoring checklists.

---

## 4. Git history as a quality asset

Git history is not just an archive. It is distributed documentation, the memory of a team's decisions, and a foundation for future analysis.

### Clean history matters

A commit like `fix stuff` is noise. A commit like `fix(auth): handle race condition in token validation (AUTH-431)` is documentation.

**Recommended format (Conventional Commits + ticket reference):**
```
<type>(<scope>): <description> (<TICKET-ID>)
```

This makes history simultaneously:
- Readable for developers
- Useful for automated changelogs and releases
- Connected to business activities

### History as technical debt

Messy history (huge commits, vague messages, mixed changes) increases the **cognitive cost of change**:
- Finding regressions requires more trial and error
- Reverting changes becomes riskier
- Refactoring is avoided out of fear

### Noisy automated PRs

Formatters and linters are essential, but when misconfigured they produce noisy commits. Preferred approach: CI fails when formatting rules are broken — developers fix before merging.

When a global formatting change is unavoidable, use a single explicit commit and register it in `.git-blame-ignore-revs` so `git blame` remains useful.

### AI-readiness

Clean history enables future AI-powered analysis: identifying files that frequently change together, modules that introduce regressions, bug patterns. Garbage history → garbage insight.

---

## 5. Entry checklist (new client assessment)

See [checklist.md](checklist.md) — it is the authoritative source for the evaluation areas, per-area questions, and priority order. Do not duplicate or redefine them here.

---

## 6. Case studies

### Case 1 — Enterprise SaaS: E2E coverage on a legacy system

**Context:** enterprise SaaS built on a legacy monolith, surrounded by a large number of microservices and micro-frontends. No E2E test coverage.

**Problem:** no automated way to verify that basic user journeys worked across the fragmented architecture. Regressions were caught by users.

**Action:** implemented a set of E2E tests in their CI pipeline using Playwright, covering the most critical user journeys.

**Result:** basic user journeys were covered with automated tests. The team gained confidence on critical paths and regressions were caught before reaching production.

**Lesson:** you don't need 100% E2E coverage. Start with the journeys that, if broken, would generate a support ticket within 5 minutes.

### Case 2 — Startup: UAT environment + feature flags

**Context:** startup with no staging/UAT environment and no feature flag system. Every code change went straight to production users.

**Problem:** developers and product managers couldn't iterate on features safely. Every experiment was a gamble. Coordination overhead was high ("don't deploy, I'm testing something").

**Action:** added a UAT environment and implemented a feature flags system.

**Result:** developers and product managers could work on features without affecting users or doing infinite coordination calls. The release process became a deliberate product decision, not a technical accident.

**Lesson:** separating deploy from release is one of the highest-ROI improvements you can make early on.
