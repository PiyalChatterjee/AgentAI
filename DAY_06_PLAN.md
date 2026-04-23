# Day 6 Plan (April 23, 2026)

## Objective
Build a practical function-calling pipeline where the model selects tools, arguments are validated with Pydantic, tools execute safely, and results are summarized back to the user.

## Timebox (4 Hours)
1. 60 min: Concept Learning (Q1-Q4)
- Q1: What is function calling and why it enables agentic systems
- Q2: Tool schema design principles for better model decisions
- Q3: How to validate and repair tool arguments safely
- Q4: Failure handling strategy (tool errors, unknown tools, malformed args)

2. 90 min: Practical Activities (A1-A4)
- A1: Define 3-5 tools with JSON schemas
- A2: Implement tool executors (calculator, web search mock, API status mock)
- A3: Add strict Pydantic validation before execution
- A4: Add fallback strategy when tool calls fail or are missing

3. 60 min: Advanced Activities (A5-A8)
- A5: Compare tool_choice modes: auto vs required vs none
- A6: Track tool-call correctness and argument validity
- A7: Add interactive mode and log tool traces
- A8: Produce a short playbook of tool schema best practices

4. 30 min: Reflection + Write-up
- Summarize what improved tool accuracy
- Document common failures and mitigations

## Deliverables
- day_06/day6_function_calling.py (to be built interactively)
- day_06/DAY_06_NOTES.md
- day_06/README.md

## Success Criteria
- Function-calling flow works in interactive mode
- Tool arguments validated at >= 95% on test prompts
- Fallback behavior is explicit and non-crashing

## Commands
```powershell
# Mentor mode: build this file step by step with guided prompts
code day_06/day6_function_calling.py
```

## Submission to Mentor
1. Tool schema table (name, inputs, failure mode)
2. Tool-choice mode comparison notes
3. Validation + fallback strategy summary
4. Final recommendations for Day 7 multimodal agent
