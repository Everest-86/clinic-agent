# QA Test Strategy

## QA objective

Prove that the AI medical voice agent is:

- operationally reliable
- safe within its approved scope
- accurate enough for real patient outreach
- observable enough for staff to trust
- resilient enough to fail safely when confidence is low

## Quality principles

### 1. Patient-safe before feature-complete

The system must never prioritize completion rate over safe escalation behavior.

### 2. Administrative-only scope

QA must verify that the agent stays inside approved administrative support and does not drift into diagnosis, emergency advice, medication changes, or clinical recommendations.

### 3. Real-world voice testing

The system must be tested against noise, pauses, accents, low-confidence audio, voicemail, and partial responses rather than only clean scripted utterances.

### 4. End-to-end traceability

Every call should be traceable across telephony, transcript, intent classification, workflow outcome, and dashboard state.

### 5. Fail safe

When the system is uncertain, it should clarify, confirm, retry carefully, or escalate to staff.

## Test layers

### 1. Unit tests

Focus on deterministic logic such as:

- patient selection rules
- appointment reminder logic
- state transition rules
- escalation decision helpers
- payload mapping and data validation

### 2. Contract tests

Validate interfaces between:

- FastAPI and frontend
- backend and Twilio webhooks
- backend and OpenAI wrappers
- backend and PostgreSQL repositories

This layer is critical because many failures in this system happen at service boundaries.

### 3. Integration tests

Validate real workflow behavior across combined components such as:

- outbound reminder creation
- confirmation persistence
- reschedule request routing
- feedback capture and storage
- escalation flag creation

### 4. End-to-end tests

Cover the most important patient journeys:

- appointment reminder to confirmation
- appointment reminder to reschedule request
- clinic-hours question handled correctly
- refill-routing request handed to the correct queue
- unsupported medical question escalated safely
- feedback captured and visible in dashboard

### 5. AI evaluation tests

This is the most important QA differentiator for this project.

Create a benchmark set of prompts and expected behaviors for:

- normal administrative requests
- ambiguous requests
- disguised clinical questions
- emotional or frustrated callers
- multilingual phrasing
- prompt-injection style attempts

Each eval should grade:

- intent accuracy
- policy compliance
- escalation correctness
- tone safety
- response usefulness

### 6. Voice quality tests

Test matrix should include:

- accents
- slow speech
- background noise
- speakerphone versus direct handset
- silence and interruptions
- repeated clarification loops
- mixed-language or language-switching scenarios

### 7. Security and privacy tests

Verify:

- least-privilege access to patient data
- safe logging and masking
- no overexposure of PHI in prompts or dashboards
- output blocking for unsafe content
- resistance to prompt injection and off-policy requests

### 8. Performance and resilience tests

Test:

- concurrent outbound call batches
- webhook spikes
- provider latency
- retries and duplicate callbacks
- STT or TTS degradation
- OpenAI timeout or fallback behavior

## Core test scenarios

### Functional

- patient confirms appointment
- patient asks to reschedule
- patient asks clinic hours or location
- patient asks insurance or billing basics
- patient leaves satisfaction feedback

### Safety

- patient asks for diagnosis
- patient reports emergency symptoms
- patient asks for dosage change
- patient asks a clinical follow-up question beyond approved scope

### Reliability

- Twilio callback arrives late
- duplicate webhook event received
- transcript confidence is low
- dashboard update fails after a successful call
- partial call completes and retry logic starts

## Test data strategy

Use synthetic patient records for:

- upcoming appointments
- pending follow-ups
- no appointment on file
- multiple appointments
- preferred language variants
- previous escalation history
- different visit types

Do not depend on real patient data for normal QA execution.

## Release gates

A release should not move forward unless:

- critical end-to-end flows pass
- AI eval suite clears agreed thresholds
- unsupported clinical prompts are escalated correctly
- dashboard outcomes match call outcomes
- no unresolved high-severity defects remain in critical flows
- observability and rollback checks are ready

## Severity model

### Severity 1

Unsafe clinical response, PHI exposure, wrong patient context, failed urgent escalation.

### Severity 2

Wrong workflow outcome, missing dashboard visibility, failed reminder completion, incorrect reschedule persistence.

### Severity 3

Recoverable conversation issue, partial logging defect, low-priority UX friction.

## What makes QA leadership strong here

The strongest QA contribution is not just writing more tests. It is building a quality model that combines:

- traditional automation
- AI evals
- voice-quality coverage
- safety guardrails
- observability-based release readiness

That is where this project needs senior QA judgment the most.
