# Day 1: OpenAI API & System Prompts Fundamentals

**Date:** April 16-17, 2026  
**Status:** ✅ Complete  
**Hours Invested:** 5-6 hours  

---

## What You'll Learn

### Q1: How the OpenAI API Works
- Request-response architecture
- Core fields: model, messages, parameters
- Conversation memory (you manage it)
- Token-based pricing

### Q2: System Prompts
- What they are and why they matter
- Good structure (role → objective → constraints → style → format)
- 3 practice examples: Friendly Teacher, Technical Expert, Product Manager
- Context-dependent prompt selection

### Q3: How to Structure an API Call in Python
- Complete anatomy: initialize → build → send → parse
- Message roles (system/user/assistant)
- Conversation history pattern
- Parameters: temperature, top_p, max_tokens
- Response structure deepdive

### Q4: Tokenization & Cost
- What tokens are (subword units)
- Why they matter (cost, context window, latency)
- How to count tokens with tiktoken
- Cost calculation and optimization

---

## Files in This Folder

| File | Purpose | Status |
|------|---------|--------|
| `DAY_01_NOTES.md` | Comprehensive concept notes (Q1-Q4) + all activities | ✅ 350+ lines |
| `day1_chatbot.py` | 3-prompt comparison chatbot | ✅ Working |
| `token_utils.py` | Token counter utility (with offline fallback) | ✅ Working |
| `day1_results.json` | Saved API responses from chatbot run | ✅ Data |

---

## Quick Start

### Prerequisites
- Python 3.x in `.venv`
- `.env` file with Azure OpenAI credentials (in root)
- Packages: `openai`, `python-dotenv`, `tiktoken`

### Run the Chatbot
Compare 3 system prompts on the same question:

```bash
cd day_01
python day1_chatbot.py
# Or test a specific prompt:
python day1_chatbot.py friendly_teacher
python day1_chatbot.py technical_expert
python day1_chatbot.py product_manager
```

**Output:** `day1_results.json` with timestamp, responses, and token counts

### Count Tokens
```bash
# Count tokens in text
python token_utils.py -t "Your text here" -p 0.0001

# Count tokens in a JSON message file
python token_utils.py -f messages.json -m gpt-4o-mini -p 0.00015
```

---

## Key Takeaways

1. **Prompt choice is context-dependent** — Same question + 3 different prompts = 3 fundamentally different outputs
2. **Explicit structure wins** — Adding constraints (word counts, bullet format) dramatically improves output
3. **Token management = cost management** — Different prompts used 231-290 tokens; always count before deploying
4. **API is stateless** — You manually manage conversation history by resending full context each call

---

## Metrics

- ✅ Task completion: 100%
- ✅ Correctness: 98% (Q3 recall: 3/4 perfect; 1 with minor clarification)
- ✅ Reliability: 100% (both scripts run end-to-end without errors)
- ✅ Artifacts: 2 production scripts + comprehensive notes

---

## For Your Review

### Learning Notes
Open `DAY_01_NOTES.md` for:
- Detailed Q&A notes with recall checks
- Activity logs and results
- Parameter deep dives (especially Temperature vs Top_P)
- Common mistakes to avoid

### Code Review
- `day1_chatbot.py` — Shows proper Azure OpenAI integration, .env loading, multi-prompt comparison
- `token_utils.py` — Demonstrates token counting with graceful offline fallback (char-based estimation)

### Next Steps
- **Practice:** Build a multi-turn conversation script reusing this setup
- **Day 2:** Model Comparison & Architecture (compare multiple models using the same framework)

---

## Questions?
See `DAY_01_NOTES.md` → Section 7: Key Takeaways & Questions for discussion points.
