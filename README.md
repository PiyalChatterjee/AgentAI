# AgentAI Transition Workspace

**30-day transition from React developer to Agentic AI engineer**

**Current Status:** Day 6 complete (April 23, 2026) | Days 1-6 ✅ | Day 7 setup ready

---

## Quick Reference: Progress Summary

| Day | Topic | Status | Key Artifact | Commits |
|-----|-------|--------|--------------|---------|
| **1** | Chatbot + token utils | ✅ Complete | `day_01/day1_chatbot.py` | ✅ Pushed |
| **2** | Model comparison + selector | ✅ Complete | `day_02/day2_model_comparison.py` | ✅ Pushed |
| **3** | Token optimization + cost analysis | ✅ Complete | `day_03/day3_token_optimization.py` + `day3_cost_report.json` | ✅ Pushed |
| **4** | Structured output + Pydantic validation | ✅ Complete | `day_04/day4_structured_output.py` + `day4_structured_output_report.json` | ✅ Pushed |
| **5** | Agentic patterns + brochure generator | ✅ Complete | `day_05/day5_agentic_react.py` + `day_05/project/main.py` | ✅ Pushed |
| **6** | Function calling & tool use | ✅ Complete | `day_06/day6_function_calling.py` + `day_06/DAY_06_NOTES.md` | ✅ Pushed |
| **7** | *Multimodal agent foundations* | 🔄 **In Progress (setup ready)** | `day_07/day7_multimodal_agent.py` (to build) | — |

---

## Environment Setup (for new system)

**Python:**
```bash
cd c:\Users\piyal.chatterjee\Documents\Projects\AgentAI
python -m venv .venv  # skip if .venv already exists
# Windows
.venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```

**Required packages:**
- `openai` — Azure OpenAI client
- `requests` — HTTP calls
- `pydantic` — JSON validation  
- `tiktoken` — Token counting
- `python-dotenv` — .env loading

**Dependency file:**
- `requirements.txt` is included at repo root for one-command install.

**Environment variables (.env file):**
```
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_ENDPOINT=<https://...>
AZURE_OPENAI_API_VERSION=2024-10-01
AZURE_OPENAI_DEPLOYMENT_NAME=ai102-chat-model
```

**Local Ollama (optional):**
- Model: `llama3.2:latest` at `http://localhost:11434`
- Start (Windows): `ollama serve`
- Start (Linux/Mac): `ollama serve`

---

## Days 1-4: What Happened

### Day 1: Chatbot Foundation
- **Q1-Q4:** System prompts, token counting, context windows, model selection
- **A1-A8:** Built 3-prompt chatbot + token utility + examples
- **Key Learning:** Token awareness prevents expensive surprises; system prompts drive consistent behavior
- **Artifact:** `day_01/day1_chatbot.py` (working chatbot with 3 personas)

### Day 2: Model Comparison & Selection
- **Q1-Q4:** Model architecture, attention mechanisms, performance metrics, router design
- **A1-A8:** Azure + Ollama unified comparison, edge-case suite, model selector by task/budget/latency
- **Key Learning:** Different models for different tradeoffs; selector routes by task type + constraints
- **Artifacts:** `day_02/day2_model_comparison.py`, `day2_edge_cases.py`, `model_selector.py`

### Day 3: Token Optimization & Cost Analysis
- **Q1-Q4:** Tokenization internals, cost dynamics, optimization techniques, quality preservation
- **A1-A8:** Built cost benchmark with 3 prompt families, profiled across pricing tiers, measured quality risk
- **Key Findings:**
  - 48.25% average token reduction via prompt compression
  - 45.78% cost reduction ($102,400 monthly savings @ 1M calls/day)
  - Quality regression floor: 120-token completion cap (medium risk)
- **Artifacts:** `day_03/day3_token_optimization.py`, `day3_cost_report.json`

### Day 4: Structured Output & JSON Validation ✅ COMPLETED TODAY
- **Q1-Q4:** Few-shot prompting (4/5), chain-of-thought safety (3.5/5), JSON mode + constraints (3.5/5), Pydantic criticality (4/5)
- **A1-A8:** Built JSON pipeline with Pydantic schema, few-shot examples, retry/repair, 20-case benchmark
- **Key Findings:**
  - Baseline (zero-shot): 100.0% validity (20/20)
  - Few-shot (with example): 100.0% validity (20/20)
  - Recommendation: Azure model strong; choose by token budget
  - Pydantic catches silent corruption that JSON syntax validation misses
- **Artifacts:** `day_04/day4_structured_output.py`, `day4_structured_output_report.json`, `day_04/DAY_04_NOTES.md`

---

## Day 7 Planning (What Needs to Happen Next)

### Scope: Multimodal Agent Foundations + Real Tool Integration
**Concept Questions (Q1-Q4):**
1. **Q1:** What changes when moving from text-only agents to multimodal agents?
2. **Q2:** How should multimodal input contracts be designed (text, image URL/path, metadata)?
3. **Q3:** What validation and safety checks are required before image/tool processing?
4. **Q4:** How do we evaluate multimodal tool-use quality and failure modes?

**Activities (A1-A8):**
- A1: Define multimodal request schema and routing contract
- A2: Implement image-analysis tool stub with strict IO shape
- A3: Add one real retrieval/data tool with timeout and retry controls
- A4: Add validation and safety checks for image/source inputs
- A5: Implement planner routing for text-only vs multimodal flows
- A6: Add JSONL metrics/traces persistence
- A7: Build quick evaluation set (10 prompts) for reliability checks
- A8: Produce Day 7 multimodal failure-mode and mitigation playbook

**Success Criteria:**
- Multimodal pipeline runs end-to-end with explicit routing visibility
- Input validation blocks unsafe/invalid image or URL payloads
- Real retrieval tool is resilient (timeout/retry/fallback) and observable

**Day 7 starter artifacts (prepared):**
- `day_07/README.md` — Day 7 mentor-mode run guide
- `day_07/DAY_07_NOTES.md` — Q1-Q4 and A1-A8 tracking template
- `DAY_07_PLAN.md` — Day 7 objective/timebox/deliverables
- `day_07/day7_multimodal_agent.py` — to be built interactively

---

## Day 6 Summary (Completed)

- Function-calling engine completed (`day_06/day6_function_calling.py`)
- Tool-choice comparison (`auto`, `required`, `none`) validated
- Metrics + trace-enabled response envelope completed

---

## Day 5 Summary (Completed)

- ReAct benchmark + Azure planner integrated
- Project 1 brochure generator completed (`day_05/project/main.py`)
- Smoke test added (`day_05/project/smoke_test.py`)

---

## Files to Review on New System

**Setup/Planning:**
- [README.md](README.md) ← You are here
- [ROADMAP_AI_AGENTIC.md](docs/ROADMAP_AI_AGENTIC.md) — Full 30-day curriculum
- [DAILY_CHECKIN_TEMPLATE.md](docs/DAILY_CHECKIN_TEMPLATE.md) — Latest check-in (Day 4)

**Day 1-4 Learning Notes (with Q1-Q4 answers + A1-A8 evidence):**
- [day_01/DAY_01_NOTES.md](day_01/DAY_01_NOTES.md)
- [day_02/README.md](day_02/README.md) + (Day 2 notes coming)
- [day_03/DAY_03_NOTES.md](day_03/DAY_03_NOTES.md)
- [day_04/DAY_04_NOTES.md](day_04/DAY_04_NOTES.md) ← Latest

**Day 1-4 Working Scripts:**
- `day_01/day1_chatbot.py` — Chatbot with 3 system prompts + token counter
- `day_02/day2_model_comparison.py` — Azure + Ollama benchmark
- `day_02/model_selector.py` — Router by task/budget/latency
- `day_03/day3_token_optimization.py` — Cost benchmark and analysis
- `day_04/day4_structured_output.py` — JSON validation pipeline with Pydantic

**Day 5 Working Script:**
- `day_05/day5_agentic_react.py` — ReAct-style loop with calculator/search/database/email/API tools and interactive mode

**Day 1-4 Report Artifacts:**
- `day_03/day3_cost_report.json` — Token/cost benchmarks and projections
- `day_04/day4_structured_output_report.json` — Validity comparison and playbook

---

## Running Day 4 (to verify setup on new system)

```bash
cd c:\Users\piyal.chatterjee\Documents\Projects\AgentAI
.venv\Scripts\activate  # or source .venv/bin/activate on Linux/Mac
cd day_04
python day4_structured_output.py --max-retries 1
```

**Expected output:**
- Console: 20/20 test cases validated, baseline + few-shot both 100% valid
- File: `day4_structured_output_report.json` generated with benchmark results

---

## Key Learning Milestones

| Concept | Day | Evidence |
|---------|-----|----------|
| Token awareness | Day 1-3 | 48% compression; cost awareness in prompting |
| Model selection | Day 2 | Router decides Azure vs Ollama by task type + constraints |
| Cost optimization | Day 3 | Measure before/after; quality regression floors matter |
| Structured output | Day 4 | Pydantic catches silent corruption; retry/repair at lower temperature |
| Agentic reasoning | Day 5 | ReAct pattern + tool use + hallucination detection |
| Function calling | Day 6 | Tool schemas + validated tool execution + fallback |
| *Multimodal foundations* | **Day 7** | Multimodal contracts + real retrieval + observability |

---

## Quick Commands Reference

```bash
# Activate venv
.venv\Scripts\activate

# Run Day 1 chatbot
cd day_01 && python day1_chatbot.py && cd ..

# Run Day 3 cost benchmark (generates day3_cost_report.json)
cd day_03 && python day3_token_optimization.py --daily-calls 1000000 && cd ..

# Run Day 4 structured output (generates day4_structured_output_report.json)
cd day_04 && python day4_structured_output.py --max-retries 1 && cd ..

# Run Day 5 benchmark (generates day5_agentic_report.json)
cd day_05 && python day5_agentic_react.py --benchmark --out day5_agentic_report.json && cd ..

# Start Day 5 interactive session
cd day_05 && python day5_agentic_react.py --interactive && cd ..

# Start Day 6 script (completed)
python day_06/day6_function_calling.py --query "search agentic ai"

# Start Day 7 mentor-mode build
cd day_07

# View latest check-in
Get-Content docs/DAILY_CHECKIN_TEMPLATE.md
```

---

## Next Steps for New System

1. **Clone/sync this repo** to the new system
2. **Set up .env** with Azure OpenAI credentials (same keys as current system)
3. **Verify Python venv** and install dependencies
4. **Run Day 4 test** (`python day_04/day4_structured_output.py`) to confirm environment
5. **Read [day_04/DAY_04_NOTES.md](day_04/DAY_04_NOTES.md)** to understand latest context
6. **Run Day 5 benchmark** (`python day_05/day5_agentic_react.py --benchmark`)
7. **Start Day 5 interactive session** (`python day_05/day5_agentic_react.py --interactive`)

---

## Contact & Support

- Daily mentor feedback: Check [docs/DAILY_CHECKIN_TEMPLATE.md](docs/DAILY_CHECKIN_TEMPLATE.md)
- Curriculum overview: [docs/ROADMAP_AI_AGENTIC.md](docs/ROADMAP_AI_AGENTIC.md)
- Code questions: Review relevant day's notes + script comments
