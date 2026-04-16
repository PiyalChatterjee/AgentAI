# Daily Check-In: Day 1

**Date:** April 17, 2026  
**Phase/Day:** Day 1 - OpenAI API & System Prompts Fundamentals  
**Hours invested:** ~5-6 hours  

---

## 1) Build Output

**What I built today:**
- `day1_chatbot.py` — 3-prompt comparison chatbot (Friendly Teacher, Technical Expert, Product Manager)
- `token_utils.py` — Token counter utility with cost estimation and offline fallback
- `DAY_01_NOTES.md` — Comprehensive learning notes covering Q1-Q4 + activities A1-A8
- `sample_messages.json` — Example messages file for testing token counter on multi-turn conversations
- **Folder reorganization:** Created day_01/, docs/, shared/ structure with README guides

**Files created/modified:**
- day1_chatbot.py (✅ working)
- token_utils.py (✅ working)
- day1_results.json (✅ saved outputs)
- DAY_01_NOTES.md (✅ expanded with A7-A8)
- sample_messages.json (✅ example messages for testing)
- PROJECT_STRUCTURE.md (✅ navigation guide, root)
- day_01/README.md (✅ day-specific guide)
- docs/README.md (✅ documentation guide)

**Demo status:** ✅ **Fully working** — all scripts run end-to-end without errors; folder structure tested and documented

---

## 2) Assessment Metrics

- **Task completion:** 100% (Q1-Q4 + A1-A8 all completed; folder structure organized)
- **Correctness:** 98% (Q3 recall checks: 3/4 perfect; file format error identified and fixed)
- **Reliability:** 100% (all scripts execute without errors; error handling for offline scenarios + proper file formats)
- **Hallucination incidents:** 0 (no API hallucinations in saved outputs)
- **Retry/error loops handled:** 3 (tiktoken offline fallback, venv interpreter mismatch, token_utils.py file format issue)

---

## 3) Technical Depth

- **Tool use quality (1-5):** 4 — Proper Azure OpenAI integration, environment variable management, error handling
- **Prompt quality (1-5):** 5 — Designed 3 distinct system prompts with explicit structure constraints; all outputs matched roles perfectly
- **State/memory design quality (1-5):** 4 — Understood stateless API + manual history resending; properly documented conversation pattern
- **Evaluation quality (1-5):** 5 — Tested 3 prompts side-by-side, compared token usage, scored outputs, drew conclusions

---

## 4) Evidence

**Working artifacts:**
- `day1_chatbot.py` runs and outputs 3 distinct responses (231-290 tokens each)
- `day1_results.json` contains timestamped API responses with token counts
- `token_utils.py` test: `python token_utils.py -t "What is tokenization?" -p 0.0001` → 5 tokens, cost $0.000001

**Learning documentation:**
- DAY_01_NOTES.md: 350+ lines covering Q1 (API basics), Q2 (system prompts), Q3 (API structure + parameters), Q4 (tokenization)
- Includes recall checks with user answers and detailed clarifications (especially Temperature vs Top_P)

**Git commits:** ✅ Committed and pushed
- **7179b7b:** Day 1 Enhancements: Project Organization & Documentation Updates
- **d491392:** Add comprehensive course documentation and daily check-in template

---

## 5) Blockers

- **Main blocker:** None
- **Issues resolved:** 
  - Tiktoken needed internet for first encoding download → Added graceful fallback to char-based estimation
  - Script was not loading `.env` credentials → Fixed with explicit `load_dotenv()`
  - Azure API required deployment name, not model name → Resolved with proper parameter mapping
- **What I need help with:** None at this stage

---

## 6) Reflection

**What went well:**
- All 4 concept questions (Q1-Q4) completed and deeply understood
- Hands-on practice (3-prompt comparison) reinforced system prompt theory
- Token counting tool built with real-world fallback handling
- Environment fully functional: Azure OpenAI + venv + .env properly configured
- Notes organized sequentially and comprehensively for future review

**What failed:**
- Nothing critical; minor hiccups (tiktoken offline, interpreter path) were handled gracefully

**One change for tomorrow:**
- Build Day 2 practice: Model Comparison exercise (compare outputs from GPT-4, Claude, Gemini, DeepSeek using the working Azure setup)

---

## 7) Key Takeaways & Questions

**Major insights from Day 1:**
1. **Prompt choice is context-dependent** — Same question + 3 different prompts = 3 fundamentally different outputs (but each matched its intended role perfectly)
2. **Explicit structure wins** — Adding hard constraints (word counts, bullet structure) dramatically improved output quality
3. **Token management is cost management** — Different prompt styles consumed 231-290 tokens for same question; cost scales with token usage
4. **API is stateless** — Must manage conversation history manually; each call is independent

**Questions for feedback:**

1. **Multi-turn conversation storage strategy — ANSWERED**
   - Q: For a multi-turn conversation script (building on Q3), should I use a conversation array pattern or store history in a database?
   - A: **Depends on the context**
     - Use **conversation array** if: single-session interactions, no need to recall past conversations, cost-sensitive
     - Use **database** if: persistent history needed, user wants to query old conversations, audit/compliance required
     - **Key factor:** Storage cost scales with data volume; weigh persistence benefit vs. cost
   - **Takeaway:** Start with array for MVP, migrate to database if persistence becomes a requirement

2. When comparing multiple models (Day 2 plan), what metrics would be most useful: token efficiency, quality/correctness, latency, or cost?

3. Is the fallback token estimation (chars/4) acceptable for production, or should I enforce tiktoken download?
