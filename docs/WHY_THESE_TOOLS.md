# Why These Tools

## Interview-ready explanation

I chose the stack based on fit for workflow reliability, integration speed, and control over quality in a healthcare-adjacent voice system.

## Python

Python was a strong fit because it lets me move quickly in backend orchestration, AI integration, and workflow logic without adding unnecessary complexity. It also has a strong ecosystem for API work, automation, and testing.

## FastAPI

I chose FastAPI because it is lightweight, fast to build with, and well suited for webhook-driven systems like telephony callbacks and internal service endpoints. It also gives clean schema support and makes service boundaries easier to test.

## PostgreSQL

PostgreSQL was the right choice because the project needs reliable structured data for patients, appointments, call outcomes, feedback, and escalations. It gives strong consistency and works well for reporting and operational dashboards.

## Twilio

Twilio was important because it solves the telephony layer well and gives mature support for outbound calling, webhook events, and voice workflow integration. That lets the project focus on patient workflow and quality instead of rebuilding phone infrastructure.

## OpenAI API

I used OpenAI for the parts that benefit from language understanding and natural response generation, especially intent analysis and bounded administrative replies. The important point is that it is used inside guardrails, not as an uncontrolled decision-maker.

## Speech-to-text and text-to-speech

These are essential because the patient experience is voice-first. Speech-to-text is needed to capture patient intent, and text-to-speech makes the system usable as a natural phone interaction rather than a button-only experience.

## React or Streamlit

I kept the dashboard choice flexible because the right answer depends on delivery goals. React is stronger if the product needs a more production-style frontend, while Streamlit is useful for moving quickly on an internal operations dashboard or prototype.

## Docker

Docker helps keep the environment consistent across development, testing, and deployment. For a project with multiple services and integrations, that matters a lot for setup speed and reproducibility.

## GitHub

GitHub gives a clean place for version control, documentation, collaboration, and CI-ready workflow setup. It also makes the project easier to present professionally.

## QA-focused answer for interviews

From a QA leadership perspective, I chose tools that support traceability, controllability, and safe integration testing. The most important thing in this project is not just building a voice agent. It is making sure the system is testable across AI behavior, telephony, data updates, dashboard visibility, and escalation safety. This stack gives enough flexibility to build the product, while still allowing strong quality gates, observability, and layered testing.
