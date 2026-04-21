# Day 4 Plan (April 20, 2026)

## Objective
Master prompt engineering for reliable structured outputs and validate model responses using Pydantic schemas.

## Timebox (4 Hours)
1. 60 min: Concept Learning (Q1-Q4)
- Q1: Few-shot prompting patterns that improve consistency
- Q2: Chain-of-thought usage and safe prompting practices
- Q3: JSON mode, schema constraints, and structured output reliability
- Q4: Why Pydantic validation is essential in production systems

2. 90 min: Practical Activities (A1-A4)
- A1: Build prompt templates that force JSON output
- A2: Extract structured fields from unstructured text
- A3: Create Pydantic schema and validate outputs
- A4: Add retry + repair logic for invalid JSON

3. 60 min: Advanced Activities (A5-A8)
- A5: Compare zero-shot vs few-shot accuracy for structured extraction
- A6: Add strict output checks and failure taxonomy
- A7: Benchmark valid JSON rate across prompt versions
- A8: Build final prompt playbook for consistent structured outputs

4. 30 min: Reflection + Write-up
- Summarize accuracy gains and common failure patterns
- Document production-ready validation strategy

## Deliverables
- day_04/day4_structured_output.py
- day_04/day4_validation_results.json
- day_04/DAY_04_NOTES.md

## Success Criteria
- Pass: >= 95% valid JSON rate over 20 runs
- Stretch: >= 99% valid JSON with retry/repair pipeline

## Commands
python day_04/day4_structured_output.py

## Submission to Mentor
1. Valid JSON rate before vs after improvements
2. Top 3 failure patterns and how they were fixed
3. Final prompt version + schema
4. Production recommendation
