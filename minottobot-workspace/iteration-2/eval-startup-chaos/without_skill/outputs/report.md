# Engineering Audit Report — Swiftly Inc
**Date:** 2026-03-26
**Team Size:** 4 engineers (3 backend, 1 frontend), no dedicated QA
**Stage:** Seed-stage SaaS, 2 years old
**Stack:** Node.js API + React frontend + PostgreSQL

## Executive Summary

Swiftly Inc is operating in a high-risk engineering posture. The team ships frequently but with minimal safety nets, resulting in roughly one user-reported incident per day. While the pace of deployment reflects a healthy bias for action, the absence of tests, staging environments, observability tooling, and formal processes creates compounding risk. The recommendations below are prioritized for a 4-person team with limited bandwidth.

## Scorecard

| Area | Score | Grade |
|---|---|---|
| Testing & Quality | 0/10 | F |
| CI/CD Pipeline | 2/10 | F |
| Deployment Safety | 2/10 | F |
| Incident Management | 3/10 | D |
| Code Review Culture | 3/10 | D |
| Observability & Monitoring | 1/10 | F |
| Environment Strategy | 2/10 | F |
| **Overall** | **1.9/10** | **F** |

## Priority 1 — This Week: Stop the Bleeding
- Install Sentry (free tier) in API + frontend for error detection before users report it
- Add uptime monitoring (UptimeRobot free tier) — 30 minutes of effort

## Priority 2 — This Sprint: Reduce Deploy Risk
- Create a staging environment on Heroku using Heroku Pipelines
- Automate deployments via GitHub Actions instead of manual `git push heroku main`

## Priority 3 — Next 2-4 Weeks: Begin Test Coverage
- Write integration tests for 3-5 critical API endpoints using Jest + supertest
- Add Playwright smoke tests for 2-3 critical frontend flows
- Add CI coverage gate (even 20% floor to start)

## Priority 4 — Next Month: Formalize Code Review
- Require 1 PR approval via GitHub branch protection (15-minute setup)
- Add minimal PR template and 24-hour review SLA

## Priority 5 — Ongoing: Incident Process
- Write a one-page incident runbook
- Track incidents in a shared log; review monthly for patterns
