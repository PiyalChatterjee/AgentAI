# Day 2 Plan (April 18, 2026)

## Objective
Understand LLM model landscape through comparative analysis and build abstraction layer for multiple model providers.

## Timebox (4 Hours)
1. **60 min: Concept Learning (Q1-Q4)**
   - Q1: How do different frontier models (GPT-4, Claude, Gemini, DeepSeek) differ architecturally?
   - Q2: What is transformer attention and how does it impact model behavior?
   - Q3: What metrics matter when comparing models: quality, cost, latency, or tokens?
   - Q4: When should you use which model for different tasks?

2. **90 min: Practical Activities (A1-A4)**
   - A1: Send same prompt to OpenAI API (GPT-4) and capture detailed response
   - A2: Test prompt with local Ollama model (if available) 
   - A3: Compare outputs on quality, token usage, cost, latency
   - A4: Build abstraction layer supporting multiple providers

3. **30 min: Advanced Activities (A5-A8)**
   - A5: Create model selector utility (task → best model)
   - A6: Build comparison table with 3+ prompts across models
   - A7: Test edge cases (complex reasoning, factual accuracy, creative tasks)
   - A8: Document findings and cost-per-task analysis

4. **30 min: Reflection + Write-up**
   - Summarize key architectural differences
   - Document when to use each model
   - Record cost/performance tradeoffs

## Deliverables
- `day2_model_comparison.py` — script that tests multiple models
- `day2_results.json` — detailed comparison outputs
- `DAY_02_NOTES.md` — comprehensive learning notes with Q1-Q4 + A1-A8
- `model_selector.py` — utility for selecting best model for task
- `comparison_table.json` — structured comparison results
- Git commit with Day 2 work

## Success Criteria (Pass/Stretch)
- **Pass:** Compare 2+ models on 3+ prompts; document differences
- **Stretch:** Automated model selector + cost analysis across all prompts

## Commands
```powershell
python day2_model_comparison.py
python model_selector.py --task "reasoning" --budget "low"
```

## Submission to Me (for assessment)
1. Comparison table (model → metric → value)
2. Three interesting findings from comparing models
3. Your recommendation for which model to use for what
4. Biggest lesson learned about model differences
