# Day 7 Plan (April 24, 2026)

## Objective
Build the first multimodal-capable agent scaffold with strong input contracts, one real retrieval tool, robust validation, and observable execution traces.

## Timebox (4 Hours)
1. 60 min: Concept Learning (Q1-Q4)
- Q1: What fundamentally changes in multimodal agent design vs text-only agents?
- Q2: How should multimodal schemas be designed for high reliability?
- Q3: What validation and safety checks must run before processing image or URL inputs?
- Q4: What are common multimodal failure modes and fallback strategies?

2. 90 min: Practical Activities (A1-A4)
- A1: Define multimodal request/response contracts with Pydantic
- A2: Implement image analysis tool stub with strict output shape
- A3: Add one real retrieval tool (HTTP-based) with timeout/retry/fallback
- A4: Add safety checks for invalid/unsafe sources and malformed payloads

3. 60 min: Advanced Activities (A5-A8)
- A5: Add planner routing (text-only vs multimodal path)
- A6: Persist metrics and traces to JSONL logs
- A7: Run 10-prompt reliability mini-evaluation
- A8: Write Day 7 multimodal failure-mode playbook

4. 30 min: Reflection + Write-up
- Summarize what improved reliability and safety most
- Document key gaps to close in Day 8

## Deliverables
- day_07/day7_multimodal_agent.py (to be built interactively)
- day_07/DAY_07_NOTES.md
- day_07/README.md

## Success Criteria
- Multimodal request pipeline executes end-to-end with clear route visibility
- Unsafe/invalid inputs are rejected before tool execution
- Retrieval path remains stable under timeout/retry conditions

## Commands
```powershell
# Mentor mode: build this file step by step with guided prompts
code day_07/day7_multimodal_agent.py
```

## Submission to Mentor
1. Multimodal schema table (field, type, constraints, failure mode)
2. Planner routing notes with sample traces
3. Retrieval reliability notes (timeout/retry/fallback outcomes)
4. Day 7 failure-mode mitigation playbook
