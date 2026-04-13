# Day 1 Plan (April 14, 2026)

## Objective
Build reliable structured output with Azure OpenAI + Pydantic and measure JSON validity.

## Timebox (3-4 Hours)
1. 30 min: Review concepts
- Tokenization basics
- Few-shot prompting
- Chain-of-thought prompting (use internally, do not expose in final outputs)
- Structured outputs and schema enforcement

2. 120 min: Coding lab
- Extend `lab1.py` into a repeatable evaluator script (`lab1_eval.py`)
- Generate 25 leads with varied prompts
- Validate every response with Pydantic
- Log pass/fail and failure reason

3. 45 min: Prompt iteration
- Create 3 prompt versions:
  - V1: simple system+user
  - V2: includes 2 few-shot examples
  - V3: strict field-level constraints in instructions
- Compare validity rates

4. 30 min: Reflection + write-up
- Summarize what improved validity the most
- Document common failure patterns

## Deliverables
- `lab1_eval.py`
- `results_day1.json`
- `DAY_01_RETRO.md`

## Success Criteria (Pass/Stretch)
- Pass: >= 96% valid JSON with Pydantic over 25 runs
- Stretch: 100% valid JSON and clear failure taxonomy

## Commands
```powershell
python lab1.py
python lab1_eval.py
```

## Submission to Me (for assessment)
Send me:
1. Validity rate
2. Two failed outputs (if any)
3. Final prompt version used
4. Biggest lesson learned
