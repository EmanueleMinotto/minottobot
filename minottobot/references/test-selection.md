# minottobot — Test Selection Guide

When someone describes a scenario and asks what kind of test to write, start from the test pyramid — not from the scenario alone.

First, evaluate the existing stack:
- **What layers exist?** Unit, integration, E2E, manual — what's present and what's missing?
- **Where are the gaps?** The most common pattern: some unit tests, heavy E2E, zero integration. The gap in the middle is usually the most impactful to fill.
- **What's the feedback speed?** If the suite takes 30 minutes, developers won't run it. Slow tests erode trust.
- **Are the tests trustworthy?** Flaky or ignored tests are worse than no tests.

Don't recommend replacing what works. If a tool is doing its job and the team knows it well, keep it. Use the decision matrix below to fill gaps — not to redesign a stack that isn't broken.

---

## Decision matrix

| Scenario | Recommended test type |
|----------|-----------------------|
| Pure function, business logic, algorithm | Unit |
| UI component with no external dependencies | Unit |
| Form validation logic | Unit |
| Database query / ORM interaction | Integration |
| REST or GraphQL endpoint (your own) | Integration |
| Multiple internal services talking together | Integration |
| Third-party API call (with a sandbox) | Integration |
| Third-party API call (no sandbox available) | Contract |
| Microservices communication / API contracts | Contract |
| Critical user journey (login, checkout, signup) | E2E |
| Regression on a bug that reached production | E2E or integration (at the level the bug lived) |
| Cross-browser behavior | E2E (multi-browser) |
| UI layout, visual appearance | Visual regression |
| Performance-sensitive code path | Performance / load test |
| Unit tests exist on critical logic, but you're not confident they'd catch a subtle bug | Mutation testing |
| Event-driven / async workflow | Integration |
| Webhook handling | Integration |
| Authentication / authorization flow | Integration + E2E (for the happy path journey) |

---

## When to use each type

### Unit tests

Use when the code under test has no external dependencies or when you can meaningfully isolate the logic.

**Best for:** pure functions, business rules, validators, parsers, state machines, utility code, component rendering logic.

**Signs you're in unit test territory:**
- You can call the function with just inputs and assert on outputs
- No database, no HTTP, no filesystem
- Feedback is instant (milliseconds)

**Watch out:** don't mock everything just to write a unit test. If the interesting behavior lives in the interaction with an external system, a unit test won't tell you much.

---

### Integration tests

Use when the behavior you care about involves two or more real components working together — a service talking to a database, a handler calling an external API, a module interacting with the filesystem.

**Best for:** API endpoints, database queries, queue consumers, service-to-service calls (with a real or in-memory version of the dependency).

**Signs you're in integration test territory:**
- The logic is simple but the interaction with infrastructure is what can break
- You need to verify that queries return the right data
- You want to test error handling for real failure modes (network errors, DB constraints)

**Watch out:** use real dependencies when possible. Mocking a database in an integration test often defeats the purpose. Use an in-memory or containerized database (Docker, Testcontainers) instead.

---

### E2E tests

Use for critical user journeys where the value of catching a regression outweighs the cost of slower feedback.

**Best for:** login, checkout, signup, core navigation, the flows that would generate a support ticket within 5 minutes if they broke.

**Signs you're in E2E territory:**
- The bug involves multiple layers (frontend, backend, database)
- The user journey is what matters, not a specific function
- You want to verify that everything works together in a real browser

**Watch out:** E2E tests are expensive. Don't use them for scenarios that integration or unit tests can cover just as well. A focused E2E suite of 20 trustworthy tests beats a bloated suite of 200 flaky ones.

---

### Contract tests

Use when two separate systems (often owned by different teams) need to agree on an interface, and you can't easily run both in the same test environment.

**Best for:** microservices communication, public APIs consumed by external clients, third-party integrations without a sandbox.

**Signs you're in contract test territory:**
- Two teams need to verify their systems are compatible without coupling their test environments
- You're a consumer of an external API that can break without notice
- You want to detect breaking changes before they reach production

---

### Visual regression tests

Use when you need to catch unintended visual changes — layout shifts, styling regressions, component appearance.

**Best for:** design systems, component libraries, UI-heavy products where visual consistency matters.

**Signs you're in visual regression territory:**
- Your users would immediately notice if something looked different
- CSS changes risk breaking layouts in unexpected places
- You have a design system that needs to stay consistent across many components

---

### Performance tests

Use when you have explicit performance requirements or when a code path is known to be latency-sensitive.

**Best for:** API response time requirements, database query performance, load-sensitive endpoints.

**Signs you're in performance test territory:**
- There's a concrete SLA to verify (e.g., "p99 must be under 200ms")
- A recent change is suspected to have introduced a slowdown
- You're about to handle significantly more traffic

**Watch out:** don't write performance tests speculatively. Write them when there's a real constraint to enforce.

---

### Mutation tests

Mutation testing doesn't test your code — it tests your tests. It works by automatically introducing small changes to the code (a `>` becomes `>=`, a `+` becomes `-`) and checking whether at least one test fails. If a mutation survives undetected, the tests aren't catching what they claim to catch.

Use it when you already have unit tests on critical logic but want to verify they're meaningful, not just present.

**Signs you're in mutation test territory:**
- Coverage is high but confidence is low — the tests feel like they're going through the motions
- The logic is financial, security-sensitive, or otherwise high-stakes, where a subtle bug slipping through has real consequences
- You've inherited a test suite and don't know whether to trust it

---

## Heuristics for ambiguous cases

**"I don't know where the bug lives."**
Start with an E2E test that reproduces the failure. Once you've reproduced it, narrow down to the layer where it actually lives and add a lower-level test there. Then delete or keep the E2E depending on whether it covers a critical journey.

**"Should I mock this dependency?"**
Ask: *is the interaction with this dependency the interesting part?* If yes, use the real thing. If the dependency is just noise (e.g., a logger), mock it.

**"The unit tests pass but something is still broken in production."**
The tests are testing the wrong thing. Add integration or E2E coverage at the level where the failure actually happens.

**"We have zero tests. Where do we start?"**
Unit tests on critical business logic first — they're the fastest to write and give immediate feedback. Then integration tests on the most-used endpoints. E2E last, covering only the most critical journeys.

**"Our E2E suite takes 45 minutes."**
That's a test pyramid problem, not an E2E problem. Identify what those tests are actually verifying and ask whether integration tests could cover the same ground at a fraction of the cost.

---

## The wrong test for the right reason

The most common mistake: using E2E tests for everything because "they test the whole system." They do — but they're slow, fragile, and expensive to maintain. The pyramid exists for a reason.

The second most common mistake: writing unit tests that mock so heavily they test nothing real. A unit test that mocks the database, the logger, the config, and the HTTP client is testing the mocking framework, not the code.

The right test is the one that:
1. Catches real failures
2. Runs fast enough that developers run it
3. Is specific enough to tell you where the failure is
