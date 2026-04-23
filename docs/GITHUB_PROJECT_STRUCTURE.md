# GitHub Project Structure

## Recommended repo layout

```text
clinic-agent/
|- backend/
|  |- app/
|  |  |- api/
|  |  |- core/
|  |  |- db/
|  |  |- models/
|  |  |- schemas/
|  |  |- services/
|  |  |- telephony/
|  |  |- ai/
|  |  |- workflows/
|  |  |- guardrails/
|  |  |- dashboard/
|  |  `- main.py
|  |- requirements.txt
|  `- Dockerfile
|- frontend/
|  |- dashboard/
|  |  |- src/
|  |  |- public/
|  |  `- package.json
|  `- Dockerfile
|- tests/
|  |- unit/
|  |- integration/
|  |- contract/
|  |- e2e/
|  |- ai_evals/
|  |- performance/
|  |- security/
|  `- fixtures/
|- docs/
|  |- ARCHITECTURE.md
|  |- GITHUB_PROJECT_STRUCTURE.md
|  |- QA_TEST_STRATEGY.md
|  `- LINKEDIN_POST.md
|- infra/
|  |- docker/
|  |- migrations/
|  `- monitoring/
|- scripts/
|  |- seed_data/
|  |- dev_tools/
|  `- load_tests/
|- .env.example
|- .gitignore
|- docker-compose.yml
`- README.md
```

## Why this structure works

### `backend/app/api`

FastAPI route definitions for staff dashboard endpoints, call webhooks, health checks, and internal admin endpoints.

### `backend/app/core`

Cross-cutting settings and utilities such as config, logging, auth helpers, and correlation IDs.

### `backend/app/db`

Database session handling, repository helpers, migrations linkage, and seed hooks.

### `backend/app/models`

ORM models for patients, appointments, call logs, escalations, feedback, and audit records.

### `backend/app/schemas`

Request and response schemas used by FastAPI and internal service boundaries.

### `backend/app/services`

Business-level services such as outreach scheduling, appointment confirmation handling, reschedule processing, and feedback persistence.

### `backend/app/telephony`

Twilio adapters, webhook parsing, outbound call logic, and retry handling.

### `backend/app/ai`

Intent classification, response generation, prompt management, evaluation utilities, and model wrappers.

### `backend/app/workflows`

End-to-end orchestration for flows such as appointment reminder, confirmation, refill routing, and escalation handling.

### `backend/app/guardrails`

Explicit policy rules that keep the system inside administrative scope and block unsafe or unsupported behavior.

### `frontend/dashboard`

Staff UI for monitoring calls, escalations, feedback, confirmations, and operational metrics.

### `tests`

Top-level test ownership keeps QA visible and prevents quality work from being buried inside implementation folders.

## Strong default file ownership

- backend engineers own application logic and integrations
- frontend engineers own dashboard UX and workflow visibility
- QA owns cross-flow coverage, quality models, eval suites, and release criteria
- shared ownership exists for contracts, observability, and incident readiness
