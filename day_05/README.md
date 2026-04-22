# Day 5: Agentic Patterns and Tool Use

Focus: build and evaluate a ReAct-style agent loop with strict tool schemas.

## Files
- DAY_05_NOTES.md: Q1-Q4 answers and A1-A8 evidence
- day5_agentic_react.py: ReAct loop, tool registry, benchmark, interactive session
- day5_agentic_report.json: Benchmark output artifact (generated)

## Quick Start
```powershell
cd day_05
python day5_agentic_react.py --benchmark --out day5_agentic_report.json
python day5_agentic_react.py --interactive
```

## Use Deployed Azure Planner
If `.env` contains `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`, and `AZURE_OPENAI_DEPLOYMENT_NAME`, you can use the deployed model to plan each ReAct step.

```powershell
cd day_05
python day5_agentic_react.py --benchmark --planner azure --out day5_agentic_report_azure.json
python day5_agentic_react.py --interactive --planner azure
```

Notes:
- `--planner rule` uses deterministic local rules (default).
- `--planner azure` calls your deployed model for next-action planning.
- If Azure planning fails at runtime, the script safely falls back to `rule` planning.

## Interactive Commands
- /tools: list available tools
- /bench: run benchmark from interactive mode
- /quit: exit
