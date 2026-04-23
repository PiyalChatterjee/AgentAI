# Day 7: Multimodal Agent Foundations

Focus: move from text-only tool calling to multimodal-ready routing with strict validation, one real retrieval connector, and stronger observability.

Mode: mentor-led interactive build. The main script will be built step by step during the session.

## Files
- DAY_07_NOTES.md: Q1-Q4 answers and A1-A8 evidence
- day7_multimodal_agent.py: to be built interactively (do not pre-generate)

## Quick Start
```powershell
cd day_07
code DAY_07_NOTES.md
```

## Environment Setup
The script expects these env variables in root .env:
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_VERSION
- AZURE_OPENAI_DEPLOYMENT_NAME

Optional for retrieval testing:
- USER_AGENT (for web requests)
- REQUEST_TIMEOUT_SECONDS (default fallback in code)

## Interactive Commands
- We will define concrete run commands during implementation.
- Start with schema design and validation tests before adding external connectors.
