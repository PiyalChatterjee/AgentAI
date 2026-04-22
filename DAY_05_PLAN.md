# Day 5 Plan (April 21, 2026)

## Objective
Build a practical ReAct-style agent loop with tool calling, schema validation, retries, and measurable benchmark metrics.

## Timebox (4 Hours)
1. 60 min: Concept Learning (Q1-Q4)
- Q1: ReAct vs chain-of-thought only
- Q2: Tool schema design and model guidance
- Q3: Multi-step loop failure modes
- Q4: Agentic production metrics and improvement loop

2. 90 min: Practical Activities (A1-A4)
- A1: Build tool registry with 5 tools
- A2: Implement reasoning + action + observation loop
- A3: Add strict tool input schemas (Pydantic)
- A4: Add retry/repair when tool calls fail

3. 60 min: Advanced Activities (A5-A8)
- A5: Benchmark ReAct vs CoT-only baseline (15 cases)
- A6: Track hallucinated tools and parameter errors
- A7: Measure success rate, token estimate, loop depth
- A8: Generate practical playbook from measured outcomes

4. 30 min: Reflection + Write-up
- Summarize failure patterns and fixes
- Document production design rules for tool use

## Deliverables
- day_05/day5_agentic_react.py
- day_05/day5_agentic_report.json
- day_05/DAY_05_NOTES.md

## Success Criteria
- Pass: ReAct success rate >= 80%
- Stretch: Tool parameter validity >= 95%

## Commands
```powershell
python day_05/day5_agentic_react.py --benchmark --out day_05/day5_agentic_report.json
python day_05/day5_agentic_react.py --interactive
```

## Submission to Mentor
1. ReAct vs CoT success table
2. Hallucination and parameter failure taxonomy
3. Loop depth distribution
4. Final tool design recommendations
