# Day 2: Model Comparison & Architecture

**Date:** April 18, 2026  
**Duration:** 4 hours  
**Focus:** Understanding model differences and building abstraction layer

## Files in This Folder

- **day2_model_comparison.py** — Main script comparing outputs from multiple models
- **model_selector.py** — Utility for selecting optimal model for a given task
- **day2_results.json** — Detailed outputs from model comparison including tokens, costs, latency
- **comparison_table.json** — Structured comparison metrics across models and prompts
- **DAY_02_NOTES.md** — Learning notes covering all concept questions (Q1-Q4) and activities (A1-A8)

## Quick Start

```powershell
# Compare models on default prompts
python day2_model_comparison.py

# Select best model for a specific task
python model_selector.py --task "creative_writing" --budget "medium"

# View comparison results
cat day2_results.json
```

## Learning Path

1. **Start here:** Answer the concept questions in DAY_02_NOTES.md (Q1-Q4)
2. **Then build:** Work through activities A1-A8 while updating notes
3. **Finally document:** Run the comparison scripts and record findings

## Key Concepts

- Model architecture differences (attention mechanisms, training data, fine-tuning)
- Cost vs performance tradeoffs
- When to use frontier vs open-source models
- Prompt abstraction for multiple providers
- Automated model selection based on task requirements
