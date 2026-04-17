# Daily Check-In: Day 2

**Date:** April 17, 2026  
**Phase/Day:** Day 2 - Model Comparison & Architecture  
**Hours invested:** ~5-6 hours  

---

## 1) Build Output

**What I built today:**
- `day2_model_comparison.py` — Unified multi-provider comparison runner (Azure OpenAI + Ollama)
- `model_selector.py` — Rule-based model routing utility by task/budget/latency/quality constraints
- `day2_edge_cases.py` — Edge-case evaluation suite (contradiction handling, cutoff honesty, balanced sensitive reasoning)
- `day2_results.json` + `comparison_table.json` — Prompt-by-prompt and aggregated comparison metrics
- `day2_edge_results.json` + `day2_edge_summary.json` — Edge-case outputs and latency reliability summary
- `DAY_02_NOTES.md` — Complete learning notes (Q1-Q4 + A1-A8) with measured outcomes

**Files created/modified:**
- day_02/day2_model_comparison.py (✅ working)
- day_02/model_selector.py (✅ working)
- day_02/day2_edge_cases.py (✅ working)
- day_02/day2_results.json (✅ generated)
- day_02/comparison_table.json (✅ generated)
- day_02/day2_edge_results.json (✅ generated)
- day_02/day2_edge_summary.json (✅ generated)
- day_02/DAY_02_NOTES.md (✅ updated with evidence)

**Demo status:** ✅ **Fully working** — all Day 2 scripts run successfully in `.venv`; Azure deployed model and local Ollama both validated

---

## 2) Assessment Metrics

- **Task completion:** 100% (Q1-Q4 + A1-A8 completed for Day 2 scope)
- **Correctness:** 98% (model outputs consistent; minor tradeoff notes on local response structure)
- **Reliability:** 100% (all benchmark and edge-case runs completed successfully)
- **Hallucination incidents:** 0 critical incidents (cutoff honesty behavior explicitly tested)
- **Retry/error loops handled:** 4 (provider timeout tuning, Ollama long-generation handling, Azure-only run validation, combined run validation)

---

## 3) Technical Depth

- **Tool use quality (1-5):** 5 — Built end-to-end benchmark pipeline with reusable provider abstraction and CLI routing
- **Prompt quality (1-5):** 4 — Good task coverage and edge-case prompts; next step is tighter output-length constraints for consistency
- **State/memory design quality (1-5):** 5 — Standardized result schema across providers and persisted structured run artifacts
- **Evaluation quality (1-5):** 5 — Compared quality, latency, tokens, and cost across baseline and edge-case suites

---

## 4) Evidence

**Working artifacts:**
- `day2_model_comparison.py` produced side-by-side benchmark metrics for Azure + Ollama
- `model_selector.py` produced consistent routing outputs for legal/support/creative/code scenarios
- `day2_edge_cases.py` produced 3/3 successful runs for each provider

**Measured benchmark summary (A3/A6):**
- **Azure deployed (`ai102-chat-model`)**
  - Avg latency: **4873.23 ms**
  - Avg tokens: **309.67**
  - Avg estimated cost: **$0.003097/prompt**
  - Avg quality (auto): **5.0/5**
- **Ollama (`llama3.2:latest`)**
  - Avg latency: **23624.63 ms**
  - Avg tokens: **245.0**
  - API cost: **$0.0** (infra/electricity not included)
  - Avg quality (auto): **4.67/5**

**Edge-case summary (A7):**
- Azure: 3/3 success, avg latency **4204.71 ms**
- Ollama: 3/3 success, avg latency **36432.9 ms**
- Notable behavior: Azure gave clearer cutoff uncertainty responses; both handled balanced argument prompts reasonably

**Learning documentation:**
- `day_02/DAY_02_NOTES.md` now includes completed concept answers, benchmark analysis, cost projections, and final recommendation matrix

**Git commits:**
- Not committed yet for Day 2 artifacts (pending your commit preference)

---

## 5) Blockers

- **Main blocker:** None remaining
- **Issues resolved:**
  - Long Ollama response times on larger prompt/model combinations → mitigated via lighter model selection and generation caps
  - Azure-only visibility gap in results → resolved with provider-specific run and combined run
  - Local vs cloud timing inconsistency → captured explicitly in benchmark and edge-case summaries
- **What I need help with:**
  - Optional: confirm final pricing constants per Azure deployment for exact (not estimated) cost reporting

---

## 6) Reflection

**What went well:**
- Completed full model-comparison learning loop from concepts to production-style evaluation scripts
- Successfully benchmarked Azure deployed model against local Ollama with consistent schema
- Built practical model routing utility aligned with task constraints (quality, latency, budget)
- Captured edge-case behavior instead of only happy-path outputs
- Notes are now sequential and review-friendly with measured evidence

**What failed:**
- Initial assumption that local model would always be faster was incorrect on current hardware; latency was significantly higher despite lower tokens

**One change for tomorrow:**
- Start Day 3 with token/cost optimization and quality-regression checks using today’s benchmark harness as baseline

---

## 7) Key Takeaways & Questions

**Major insights from Day 2:**
1. **Model choice is a routing problem** — no single model wins on all dimensions (quality, latency, cost)
2. **Lower token count does not guarantee lower latency** — compute environment and inference stack matter heavily
3. **Cloud model currently wins UX in this setup** — Azure was ~4.9x faster on average than local Ollama benchmark runs
4. **Edge-case behavior matters for trust** — explicit uncertainty handling is a key quality signal

**Questions for feedback:**

1. For production routing, should I add confidence scoring + automatic fallback (e.g., local first, Azure fallback on low confidence)?
2. Should I prioritize batching/parallelization next for throughput optimization, or prompt-compression first for cost optimization?
3. For cost reporting, is an estimated per-1K token constant acceptable at this stage, or should I integrate deployment-specific pricing config now?
