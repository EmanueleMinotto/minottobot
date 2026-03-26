# Engineering Quality Audit Report
## FinanceCore Ltd — Phase 0 Assessment

**Date:** 2026-03-26
**Scope:** Engineering practices, CI/CD pipeline, test quality, incident management, and delivery cadence
**Data Source:** Phase 0 questionnaire responses

---

## Executive Summary

FinanceCore Ltd is a 20-year-old financial services company operating a substantial engineering organisation of 85 engineers across 8 product teams. The assessment reveals a pattern consistent with long-established enterprises: technically capable teams hampered by accumulated process debt, aging infrastructure, and organisational structures that were appropriate at an earlier scale but now impose friction on delivery velocity and quality.

**Overall Assessment: Moderate Risk / High Improvement Potential**

The organisation has a solid foundation — reasonable test coverage numerically, an established code review policy, and a recognisable microservices architecture — but several systemic issues require structured remediation. The most critical concerns are test reliability (30% flakiness), CI pipeline age and speed (47-minute builds on a 2011 Jenkins setup), and deployment process rigidity (6-hour biweekly windows with manual sign-offs). These three issues compound one another and significantly limit engineering throughput and confidence.

---

## 1. Team Structure and Quality Ownership

### Findings

| Dimension | Current State | Industry Benchmark |
|---|---|---|
| Engineers per team | ~10–11 avg (85 / 8 teams) | 5–10 (optimal) |
| QA coverage | 6 central QA for 85 engineers | 1 QA per 5–8 engineers |
| QA-to-engineer ratio | 1:14 | 1:5–1:8 |

### Analysis

The centralised QA guild model (6 QA professionals serving 85 engineers) creates a significant quality bottleneck. At a 1:14 ratio, the QA guild cannot provide meaningful pre-release coverage across all 8 product teams simultaneously. This structural gap typically manifests in two ways:

1. **Deferred quality work:** Teams ship features without adequate QA involvement, relying on central QA only at release gates, creating late-cycle defect discovery.
2. **Quality abdication:** Product teams treat quality as "QA's problem," reducing developer ownership of testing, which contributes directly to the observed test flakiness.

The team size of ~10–11 engineers per team is at the upper end of what allows effective communication. Some teams may be experiencing coordination overhead that reduces effective output per engineer.

### Recommendations

- **Embed quality champions** within each product team — engineers with QA skilling who own test strategy at the team level, without necessarily moving headcount from the central guild.
- **Shift quality ownership left:** Introduce team-level quality KPIs (flakiness rate, coverage thresholds, incident contribution rate) tracked per team.
- **Redefine the central QA guild's remit** from execution to enablement: tooling, standards, training, and cross-team test strategy rather than direct test execution.

---

## 2. Test Suite Health

### Findings

| Metric | Value | Assessment |
|---|---|---|
| Total tests | ~12,000 | Reasonable for the org size |
| Flaky tests | ~3,600 (30%) | Critical — industry threshold is <2% |
| Effective reliable tests | ~8,400 | Actual safety net significantly smaller than reported |
| Flaky test disposition | "Frequently ignored" | Severe — negates CI signal |

### Analysis

A 30% flakiness rate is a serious indicator of test suite decay. More critically, the note that flaky tests are "frequently ignored" represents the most damaging state a test suite can be in: the team has implicitly accepted that CI signal is unreliable, which means the entire CI gate loses its value as a quality checkpoint.

This creates a self-reinforcing negative cycle:
- Flaky tests produce false failures
- Engineers learn to re-run and ignore failures
- Real failures are masked by assumed flakiness
- Confidence in the test suite deteriorates
- Investment in writing new tests decreases
- Coverage stagnates or erodes

In a financial services context, this is particularly concerning. Regulatory and audit requirements in financial services often assume that automated tests are a meaningful control. A 30% flakiness rate undermines that assumption and creates potential compliance exposure.

Common root causes for this level of flakiness in a Java Spring Boot / Oracle / React stack:
- **Integration tests with real database state** (Oracle DB state not properly isolated between tests)
- **Timing-dependent tests** (async operations, sleep-based waits)
- **Shared test environments** (tests interfering with each other via shared state)
- **External service dependencies** not properly mocked
- **React frontend tests** with DOM/timing sensitivity

### Recommendations

**Immediate (0–30 days):**
- Quarantine the known flaky tests into a separate suite that does not block CI. This does not fix the tests but immediately restores CI signal integrity.
- Assign a "flaky test task force" — a rotating assignment of engineers for 2-week sprints dedicated solely to flaky test remediation.

**Short-term (1–3 months):**
- Introduce a flakiness tracking dashboard. Measure flakiness rate per test, per team, per module.
- Set a hard rule: no new flaky tests permitted to merge. Any test that fails intermittently in PR validation must be fixed before merge.
- Classify the 3,600 flaky tests by root cause category and prioritise by risk (financial logic tests first).

**Medium-term (3–6 months):**
- Achieve flakiness rate below 5%, then target below 2%.
- Introduce contract testing for inter-service boundaries (Pact or similar) to replace fragile integration tests.
- Implement database test isolation strategy (e.g., @Transactional rollback, TestContainers for Oracle-compatible testing).

---

## 3. CI/CD Pipeline

### Findings

| Metric | Value | Assessment |
|---|---|---|
| CI platform | Jenkins (est. 2011) | Significantly outdated |
| Full build duration | 47 minutes | Poor — target is <15 minutes |
| CI ownership | Dedicated "CI team" | Centralised bottleneck risk |
| Deployment frequency | Biweekly | Low — industry leaders deploy multiple times daily |
| Deployment duration | 6 hours | Very high |
| Manual sign-offs | Yes | Process overhead, single point of failure |

### Analysis

**CI Pipeline Age and Speed**

A 47-minute full build on a Jenkins instance set up in 2011 is a significant productivity drag. Assuming 85 engineers each trigger 3–5 CI runs per day (including PR validation and retries), the organisation is consuming approximately 170,000–280,000 engineer-minutes per month simply waiting for CI feedback. At even a conservative fully-loaded cost, this represents substantial waste.

More critically, long feedback loops change engineering behaviour: engineers context-switch while waiting, batch multiple changes before pushing (reducing the granularity of change and increasing merge risk), and mentally "move on" before CI results arrive — reducing the probability that they act on failures promptly.

The dedicated "CI team" model, while ensuring expertise, creates a structural dependency. Product teams likely cannot self-serve CI improvements, meaning pipeline optimisation competes with CI team's other priorities and may be permanently deprioritised.

**Deployment Process**

A biweekly release window with a 6-hour deployment process and manual sign-offs is characteristic of a change management model designed for monolithic systems deployed infrequently. For a microservices architecture, this model:

- Negates the primary advantage of microservices (independent deployability)
- Creates large batched deployments that increase blast radius per release
- Means the average lead time from code-complete to production is 7–14 days
- Manual sign-offs create human bottlenecks that are unavailable outside business hours, making incident recovery slower

The 6-hour deployment duration suggests either: insufficient automation, sequential deployment of services that could be parallelised, manual environment validation steps, or Oracle DB migration processes that are not automated.

### Recommendations

**CI Pipeline:**
- **Parallelise the build.** A 47-minute build should be broken into parallel stages (compile, unit tests, integration tests, frontend build, security scans). Target: 15–20 minutes in 3 months, under 10 minutes in 6 months.
- **Introduce build caching.** Gradle/Maven dependency caching, Docker layer caching, and incremental compilation can cut build times by 30–50% with minimal investment.
- **Evaluate modern CI platforms.** Jenkins 2011 carries significant maintenance overhead. GitHub Actions, GitLab CI, or Buildkite should be evaluated. Migration can be phased by team.
- **Distribute CI ownership.** Each team should own their pipeline-as-code (Jenkinsfile or equivalent), with the CI team providing shared libraries and governance — not acting as the single operator.

**Deployment Process:**
- **Introduce continuous deployment to non-production environments immediately.** Every merge to main should automatically deploy to a staging environment without human intervention.
- **Automate deployment pipeline for production.** Manual sign-offs should be replaced by automated quality gates: test pass rate, coverage thresholds, performance regression checks.
- **Increase deployment frequency progressively.** Biweekly → weekly → on-demand. The path requires improving test confidence first (see Section 2).
- **Decompose the 6-hour deployment.** Map every step of the current deployment process. Identify which steps are sequential vs. could be parallelised, which are manual vs. automatable, and which are compensating for missing upstream quality controls.
- **Automate database migrations.** If Oracle DB migrations are manual or semi-manual, adopt Flyway or Liquibase with automated migration validation in CI.

---

## 4. Incident Management

### Findings

| Metric | Value | Assessment |
|---|---|---|
| P1 incidents/month | 2 | Elevated for financial services |
| P2 incidents/month | 1 | Acceptable but improvable |
| MTTR | ~4 hours | Poor — target is <1 hour for P1 |
| Total incident impact/month | ~10 hours of major degradation | Significant customer and regulatory risk |

### Analysis

**Incident Frequency**

Two P1 incidents per month in financial services is a material concern. Financial services firms typically face regulatory scrutiny on availability and resilience. Depending on FinanceCore's regulatory regime (FCA, SEC, etc.), repeated P1 incidents may trigger reporting obligations or regulatory findings.

The causal chain linking other findings to incident frequency is direct:
- A flaky, distrusted test suite → defects escape to production
- Biweekly batched deployments → large change sets with higher defect density per release
- 47-minute CI → engineers bypass or rush through quality gates under pressure
- Central QA bottleneck → insufficient pre-production validation

**MTTR**

A 4-hour MTTR for P1 incidents is high. Common contributing factors in this type of organisation:
- Lack of feature flags or quick rollback capability (exacerbated by 6-hour deployments — rolling back is as slow as rolling forward)
- Distributed microservices with insufficient distributed tracing and observability
- Unclear ownership during incidents (8 teams, no dedicated on-call structure apparent)
- Oracle DB as potential recovery bottleneck (rollbacks of DB migrations are notoriously complex)

### Recommendations

**Immediate:**
- Establish a post-mortem process if not already in place. Every P1 and P2 should produce a written blameless post-mortem with action items tracked to completion.
- Implement a structured on-call rotation with clear escalation paths per product area.

**Short-term:**
- **Reduce MTTR through observability investment.** Distributed tracing (OpenTelemetry), structured logging aggregation (ELK/Splunk), and alerting dashboards should be treated as P1 priorities themselves. The goal is to reduce mean time to detection (MTTD) and mean time to diagnose.
- **Implement feature flags.** A feature flag system (LaunchDarkly, Unleash, or self-built) enables instant rollback of specific features without full deployment, dramatically reducing MTTR.
- **Build a runbook library.** For recurring incident patterns, documented runbooks with step-by-step remediation reduce the cognitive load on on-call engineers and cut MTTR.

**Medium-term:**
- Target P1 frequency reduction to 0–1/month within 6 months through upstream quality improvements.
- Target MTTR reduction to under 1 hour within 6 months.
- Consider chaos engineering practices (Chaos Monkey, controlled fault injection) to find and fix resilience gaps proactively.

---

## 5. Code Review and Development Process

### Findings

| Metric | Value | Assessment |
|---|---|---|
| Required approvals | 3 | High — may introduce friction |
| Policy adherence | Some teams skip for "hotfixes" | Policy erosion — significant risk |
| Formal policy | Yes | Good foundation |

### Analysis

**Policy Adherence**

The "hotfix bypass" pattern is the most critical finding in this section. In financial services, hotfixes are typically applied during or immediately after incidents — the highest-risk moments, when the pressure to act quickly is greatest and the potential for compounding errors is highest. Bypassing code review for hotfixes removes the last human check at exactly the time it is most needed.

This pattern also typically signals a deeper issue: the normal code review and deployment process is too slow for emergency response. If engineers are bypassing review because the alternative (a full biweekly deployment with 3 approvals and a 6-hour deployment window) is genuinely impractical in an incident, then the process itself is the problem that needs fixing — not just the bypass behaviour.

**Three Required Approvals**

Three approvals is on the high end. While thoroughness is valued, this creates:
- Slower PR cycle times (3 reviewers must all be available and prioritise the review)
- Reviewer diffusion of responsibility (with 3 required, each reviewer may do less thorough review assuming others will catch issues)
- Pressure to bypass the process under time constraints (contributing to the hotfix bypass pattern)

Research in software engineering (including studies by Google and Microsoft) consistently shows that 1–2 thorough reviewers provide better outcomes than 3+ superficial reviews.

### Recommendations

- **Formalise a hotfix process that includes review.** A "fast-track" review process with 1 required approval (senior engineer or team lead) and immediate deployment capability, but with mandatory post-hoc review and documentation, preserves both speed and auditability.
- **Reduce required approvals to 2** for standard PRs, with clear expectations that each reviewer performs a thorough review.
- **Implement branch protection rules** that technically enforce review requirements — making it impossible (not just discouraged) to bypass code review without an explicit emergency override recorded in the audit log.
- **Track policy adherence as a metric.** Report monthly on bypass rate per team. Treat repeated bypasses as a process problem to solve, not a discipline problem to police.

---

## 6. Technology Stack Assessment

### Findings

| Component | Technology | Assessment |
|---|---|---|
| Backend | Java Spring Boot microservices | Solid, industry-standard |
| Database | Oracle DB | Legacy, high cost, migration risk |
| Frontend | React | Current, good ecosystem |
| CI | Jenkins (2011) | Outdated, migration candidate |

### Analysis

**Java Spring Boot Microservices**

Spring Boot is a mature, well-supported framework appropriate for financial services. The microservices architecture is conceptually sound but requires operational maturity (service mesh, distributed tracing, contract testing) to realise its benefits. Without this operational layer, microservices can create more complexity than a monolith without corresponding agility benefits.

**Oracle DB**

Oracle is a significant strategic risk for the following reasons:
- Licensing costs are substantial and scale with usage
- Oracle DBA expertise is increasingly scarce and expensive
- Schema migrations are more complex than with modern databases, contributing to deployment duration
- The lock-in is deep — migration away from Oracle is a multi-year effort

Near-term, FinanceCore should not attempt Oracle migration, but should:
- Ensure all schema changes are managed via automated migration tooling (Flyway/Liquibase)
- Avoid new Oracle-specific features that deepen lock-in
- Begin architectural planning for eventual migration to PostgreSQL or a cloud-native equivalent

**React Frontend**

React is appropriate. No immediate concerns, though the team should ensure:
- Frontend tests are included in the CI pipeline with appropriate coverage
- Frontend deployments can be decoupled from backend deployments where possible

---

## 7. Risk Summary Matrix

| Risk Area | Severity | Likelihood | Priority |
|---|---|---|---|
| Test flakiness undermining CI signal | High | Confirmed | P0 — Immediate |
| Hotfix bypass of code review | High | Confirmed | P0 — Immediate |
| 47-minute CI blocking developer flow | High | Confirmed | P1 — Short-term |
| Biweekly deployments limiting agility | High | Confirmed | P1 — Short-term |
| QA bottleneck / 1:14 ratio | Medium | Confirmed | P1 — Short-term |
| 4-hour MTTR P1 incidents | High | Confirmed | P1 — Short-term |
| 2x P1/month production incidents | High | Confirmed | P1 — Short-term |
| Oracle DB migration complexity | Medium | Confirmed | P2 — Medium-term |
| Jenkins platform age and fragility | Medium | Confirmed | P2 — Medium-term |
| Insufficient distributed observability | Medium | Inferred | P1 — Short-term |
| Missing feature flag / rollback capability | Medium | Inferred | P1 — Short-term |

---

## 8. Recommended Improvement Roadmap

### Phase 1: Stabilise (0–60 days)

Objective: Stop the bleeding. Restore CI signal integrity and eliminate the most dangerous process gaps.

1. **Quarantine flaky tests** — separate suite, no longer blocking CI merges.
2. **Formalise emergency/hotfix process** — 1-approver fast track with audit trail, not zero-approver bypass.
3. **Establish post-mortem practice** — mandatory for all P1/P2 incidents, blameless format, tracked action items.
4. **Map the deployment pipeline in detail** — document every manual step, owner, and duration. This is prerequisite to automation.
5. **Stand up a flakiness dashboard** — visualise the problem before fixing it.

### Phase 2: Accelerate (2–4 months)

Objective: Increase delivery velocity and test suite reliability.

1. **Parallelise CI pipeline** — target 20-minute builds.
2. **Remediate top 50% of flaky tests** — focus on financial logic and P1 contributing modules first.
3. **Introduce continuous deployment to staging** — automated, triggered on merge to main.
4. **Embed quality champions** in each product team.
5. **Automate database migrations** with Flyway/Liquibase.
6. **Implement distributed tracing** (OpenTelemetry + backend of choice).

### Phase 3: Optimise (4–9 months)

Objective: Achieve engineering organisation operating at modern standards.

1. **Migrate CI to modern platform** (GitHub Actions or equivalent).
2. **Increase production deployment frequency** to weekly, then on-demand.
3. **Implement feature flags** for all new features — enabling fast rollback and progressive rollouts.
4. **Achieve <5% test flakiness** across the full suite.
5. **Target 0–1 P1 incidents/month**, MTTR under 1 hour.
6. **Evaluate team structure** — consider whether 8 teams of ~10 should be restructured into smaller, more autonomous teams with broader quality ownership.

---

## 9. Metrics to Track

To assess progress, the following metrics should be captured and reviewed monthly:

| Metric | Current | 3-Month Target | 6-Month Target |
|---|---|---|---|
| CI build duration (full) | 47 min | 25 min | 12 min |
| Test flakiness rate | 30% | 15% | <5% |
| Deployment frequency | Biweekly | Weekly | On-demand |
| Deployment duration | 6 hours | 3 hours | <30 min |
| P1 incidents/month | 2 | 1 | 0–1 |
| MTTR (P1) | 4 hours | 2 hours | <1 hour |
| Code review bypass rate | Unknown | Measured | <1% |
| Lead time (commit to production) | ~7–14 days | 3–5 days | <1 day |

---

## 10. Conclusion

FinanceCore Ltd presents a profile common to financial services organisations of its vintage: technically capable engineers working within process and tooling constraints that have not kept pace with the scale and complexity of the current engineering organisation. The risk profile is elevated by the combination of high test flakiness, slow deployments, and a biweekly release cadence — all of which reduce the organisation's ability to detect and respond to quality issues quickly.

The good news is that the remediation path is well-understood and achievable. None of the issues identified are novel or require greenfield architectural work to begin addressing. The most impactful near-term investment is restoring trust in the test suite — once engineers believe CI signal is reliable, the feedback loops that support quality improvement begin to operate effectively. Everything else follows from that foundation.

The organisation has the scale, the technical stack, and the structural ingredients to operate at a significantly higher level of engineering maturity within 6–9 months with focused, sequenced effort.

---

*Report generated: 2026-03-26*
*Assessment type: Phase 0 — Observational, based on self-reported data*
*Confidence note: Findings marked "Inferred" are based on patterns typically associated with the confirmed findings and should be validated in Phase 1 discovery.*
