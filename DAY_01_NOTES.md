# Day 1 Notes Log

Date: April 16-17, 2026
Track: OpenAI API and System Prompts Fundamentals

## How this log will be maintained
- After each answered concept question, add: summary, key terms, and recall checks.
- After each completed activity, add: what was done, result, errors, and fix.
- Keep entries short and testable so revision is fast.

---

# Q&A NOTES (Concepts)

## Q1: How the OpenAI API works

**Summary:**
- OpenAI API is a request-response interface: app sends messages, model returns a completion.
- Core request fields are model, messages, and generation parameters.
- Conversation memory is not automatic; your app must resend relevant history.

**Key terms:**
- messages, roles (system/user/assistant), temperature, max_tokens, usage

**Mental model:**
- system sets behavior, user asks task, assistant responds.
- cost is based on input + output tokens.

**Recall checks:**
1. Why does a second API call need previous context messages?
2. Which two parameters most affect creativity and response length?

---

## Q2: What a system prompt is

**Summary:**
- System prompt is the highest-priority behavior instruction for the model in a conversation.
- It defines role, constraints, style, and output format.
- Strong system prompts improve consistency and reduce drift.

**Good structure:**
1. Role
2. Objective
3. Constraints
4. Style
5. Output format

**Common mistakes:**
- vague instructions
- conflicting rules
- missing output schema

**Recall checks:**
1. What is the best 1-line role statement for your Day 1 chatbot?
2. If user asks for a different tone, when should system rules still win?

**Key Lesson Learned (from practice):**
**Prompt choice is context-dependent.** The "best" system prompt depends on:
1. Audience expertise level
2. Goal (learn vs. build vs. pitch)
3. Required depth and formality

Same user question produces wildly different outputs based on role. This is the power of system prompts—they're not good/bad, they're matched-to-purpose or mismatched.

---

## Q3: How to structure an API call in Python

**Summary:**
- API call anatomy: initialize client → build request dict → send call → parse response
- `model`: Which deployment/model to use
- `messages`: Array of role/content dicts (system first, then conversation history)
- `temperature`: Controls randomness (0=deterministic, 1.0=balanced, 2=creative)
- `max_tokens`: Limits response length
- Response structure: choices[0].message.content = answer text; usage.total_tokens = token count

**Core structure:**
```python
client = AzureOpenAI(api_key=..., api_version=..., azure_endpoint=...)
response = client.chat.completions.create(
    model="deployment-name",
    messages=[
        {"role": "system", "content": "behavior rules"},
        {"role": "user", "content": "question"}
    ],
    temperature=0.7,
    max_tokens=150
)
text = response.choices[0].message.content
tokens = response.usage.total_tokens
```

**Three message roles:**
1. **system**: Behavior instructions (always first, once per conversation)
2. **user**: Human questions/commands
3. **assistant**: Previous AI responses (fills conversation history)

**Conversation memory pattern:**
- Call 1: Send system + user question → Get response
- Call 2: Send system + user + assistant response + new user question → Get response
- API does NOT remember; YOU must resend full history

**Parameters deep dive:**
- **temperature** (0-2): Randomness via softmax reweighting (default 0.7)
  - 0 = always pick most likely token (deterministic)
  - 0.7 = balanced variety
  - 1.5+ = creative but may be incoherent
- **top_p** (0-1): Nucleus sampling; only consider tokens in top P% of probability (default 1.0)
  - Usually leave at 1.0
  - Lower values filter out weird/rare tokens
  - Use when combined with temperature for "creative + clean" output
- **max_tokens**: Response length cap

**Response structure:**
```
response
├── choices[0]
│   ├── message
│   │   ├── content         ← Answer text
│   │   └── role            ("assistant")
│   └── finish_reason       ("stop", "length", etc.)
└── usage
    ├── prompt_tokens       ← Input tokens
    ├── completion_tokens   ← Output tokens
    └── total_tokens        ← Sum
```

**Temperature vs Top_P:**
| Aspect | Temperature | Top_P |
|--------|-------------|-------|
| Mechanism | Softmax reweighting | Cumulative probability filter |
| Range | 0-2 | 0-1 |
| Use case | General creativity | Eliminate tail tokens |
| Default action | Use it (critical) | Keep at 1.0 (off) |
| When to use together | Rarely | Combine for creative + clean |

**Common mistakes:**
1. Forgetting load_dotenv() before accessing .env variables
2. Not sending conversation history in call #2
3. Extracting response wrong (response.content vs response.choices[0].message.content)

**Recall checks (user answers):**
1. Q: First required field in request? A: model ✓ (also messages; both required)
2. Q: Why send full history? A: API is stateless, no memory ✓✓ Correct
3. Q: Extract token count? A: response.usage.total_tokens ✓✓ Correct
4. Q: Temperature vs top_p? A: nucleus sampling ✓ (Explained above in detail)

---

## Q4: Why tokenization matters

**Summary:**
- Tokens are the model's atomic text units (subwords).
- Short words = 1 token; long words split into multiple tokens.
- Cost is based on input + output tokens used, not characters.
- Context window is fixed token limit; more tokens = less room for context.

**Why tokens matter:**
1. **Cost**: Providers bill per 1000 tokens. Different tokens usage = different cost.
2. **Context window**: Model has fixed token budget. Longer prompts consume budget faster.
3. **Latency**: More tokens → longer processing time.
4. **Optimization**: Shorter, tighter prompts = lower cost and faster response.

**Quick mental model:**
- 1 token ≈ 4 characters in English (rough; depends on text structure).
- 1,000 tokens ≈ 750 words.

**How to count tokens using tiktoken:**
```python
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o-mini")
text = "Explain tokenization to me."
tokens = enc.encode(text)
print(len(tokens))  # token count
```

**For chat messages:**
```python
messages = [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "What is tokenization?"}
]
# Use num_tokens_from_messages() to count (handles special tokens)
```

**Cost calculation:**
```
cost = (total_tokens / 1000) * price_per_1k_tokens
```
Example: 250 tokens at $0.0001/1k = (250 / 1000) * 0.0001 = $0.000025

**Optimization techniques (lower token usage):**
- Remove verbose context; send summarized key facts instead.
- Use compact formats (short JSON keys, minimal examples).
- Trim system prompts; keep rules but make concise.
- Cache and reuse retrieved facts; only send deltas.
- Store metadata locally; only transmit changes.

**When to optimize vs not:**
- Optimize when: high volume → cost matters, real-time → latency matters.
- Don't optimize when: one-off runs, clarity more important than micro-cost.

**Recall checks:**
1. If 1 token ≈ 4 chars, how many tokens in "Understand AI models"?
2. Why does context window matter for long conversations?
3. What's the cost of 500 tokens at $0.00015/1k?

---

# ACTIVITY LOG (Hands-On)

## Activity A1: Concept session on OpenAI API fundamentals
**Status:** Completed  
**Outcome:**
- Understood request-response cycle, roles, basic parameters, and token-based pricing model.

---

## Activity A2: Concept session on system prompts
**Status:** Completed  
**Outcome:**
- Understood instruction hierarchy and how to design stable prompt behavior.

---

## Activity A3: System prompt practice (3 styles tested)

### A3.0: Practice decision — Where to test
**Recommendation:**
- Use Copilot chat first for fast iteration of prompt wording.
- Use Ollama second to test model-specific behavior and local setup.
- Use Python script as final source of truth for reproducible results.

**Why this sequence:**
- Copilot chat is fastest for idea refinement.
- Ollama is best to understand local-model variability.
- Scripted runs are required for repeatable evaluation and later comparison.

**Mini protocol:**
1. Keep one fixed user question.
2. Run the same question with 3 system prompts.
3. Save response quality notes: clarity, correctness, tone match, and actionability.
4. Pick the winning prompt and carry it into the chatbot script.

---

### A3a: System prompt practice attempt 1-v1 (Friendly Teacher, initial)
**Status:** Completed  
**Quick score:**
- Tone alignment: 5/5
- Correctness: 4/5
- Actionability: 4/5
- Concision: 3/5

**Issue:** response drifted and was slightly verbose.

---

### A3b: System prompt practice attempt 1-v2 (Friendly Teacher, refined)
**Status:** Completed  
**Refined prompt applied:**
```
you are a teacher
explain to me openAI as a newly admitted student
use exactly 8 bullets, each bullet max 14 words
"Bullet 1: one-line definition"
"Bullets 2-4: practical uses"
"Bullets 5-6: limitations/safety"
"Bullet 7: example"
"Bullet 8: recap"
no headings, no subsections
use polite and simple terms to explain
give the output in bullet terms
```

**Output quality v2:**
- Tone alignment: 5/5
- Correctness: 5/5
- Actionability: 5/5
- Concision: 5/5
- Structure adherence: 5/5

**Result:** Perfect output. Added hard constraints dramatically improved quality and concision.

**Key lesson:**
- Explicit structure beats implicit guidance.
- Word limits force clarity.
- Bullet-by-bullet instructions eliminate drift.

---

### A3c: System prompt practice attempt 2 (Strict Technical Expert)
**Status:** Completed  
**Prompt applied:**
```
you are a senior AI research engineer
explain openAI with technical precision and depth
use exactly 8 bullets, each bullet max 14 words
"Bullet 1: technical definition"
"Bullets 2-4: architectural components or key innovations"
"Bullets 5-6: limitations or research challenges"
"Bullet 7: cite one foundational paper or concept"
"Bullet 8: research direction summary"
no explanatory text before bullets
assume audience has CS fundamentals
give output as numbered bullets only
```

**Output quality scores:**
- Tone alignment: 5/5 (precise, technical, research-focused)
- Correctness: 5/5 (accurate transformer/RLHF details)
- Actionability: 4/5 (deep but assumes expertise)
- Concision: 5/5 (exactly 8 bullets, tight wording)

**Key strengths:**
- Cites foundational concepts (Attention, Vasswani et al. 2017)
- Discusses RLHF, fine-tuning, preference optimization
- Addresses hallucinations and research challenges
- Best for: engineers, researchers, technical interviews

---

### A3d: System prompt practice attempt 3 (Product Manager)
**Status:** Completed  
**Prompt applied:**
```
you are a product manager at a tech company
explain openAI from market and user value perspective
use exactly 8 bullets, each bullet max 14 words
"Bullet 1: market positioning in one sentence"
"Bullets 2-4: customer pain points this solves"
"Bullets 5-6: competitive advantages or moat"
"Bullet 7: pricing or business model insight"
"Bullet 8: future product direction prediction"
no headers, no fluff
focus on business impact and outcomes
output as bulleted list only
```

**Output quality scores:**
- Tone alignment: 5/5 (business-focused, outcomes-driven)
- Correctness: 5/5 (accurate market positioning and moats)
- Actionability: 5/5 (clear business case and ROI)
- Concision: 5/5 (tight, persuasive bullets)

**Key strengths:**
- Focuses on productivity, cost savings, 24/7 availability
- Explains ecosystem lock-in via APIs and integrations
- Revenue model clarity (subscription + enterprise SLAs)
- Best for: investors, product strategy, business pitches

---

### A3e: Final Comparison & Routing Rules

| Context | Best Prompt | Why |
|---------|------------|-----|
| Teaching concepts/fundamentals | Friendly Teacher | Accessible, beginner-friendly, structured learning |
| Deep technical insights | Strict Technical Expert | Precise, research-backed, assumes expertise |
| Product/business understanding | Product Manager | Outcome-focused, ROI clarity, market context |

---

## Activity A4: First working chatbot run (3-prompt comparison executed)
**Status:** Completed  
**Date:** April 16, 2026

**Setup:**
- Fixed: Added load_dotenv() to load .env credentials
- Fixed: Changed model parameter to deployment name "ai102-chat-model"
- Installed: python-dotenv and openai packages in venv
- Environment: Azure OpenAI with gpt-4o-mini-2024-07-18

**Results executed:**
- Friendly Teacher: 231 tokens, good structure and tone
- Technical Expert: 264 tokens, precise technical details with foundational papers
- Product Manager: 290 tokens, focused on market positioning and business value

**Output saved:** day1_results.json

**Observations:**
1. Different prompts produced distinctly different outputs for same user question
2. Token usage varied (231-290) - more detailed prompts consumed more tokens
3. All outputs matched their designed roles perfectly
4. Finish reason: all "stop" = clean completions

**Key lesson:**
System prompts create dramatically different outputs BUT **cost varies with token usage**. Token management matters for budgeting.

---

## Activity A5: Token counting tool created and tested
**Status:** Completed  
**File:** `token_utils.py`

**Features:**
- Counts tokens from text (-t flag) or JSON message files (-f flag)
- Loads deployment name from `.env` (AZURE_OPENAI_DEPLOYMENT_NAME)
- Estimates cost based on token count and per-1k price
- Fallback estimation when tiktoken unavailable (1 token ≈ 4 chars)

**Usage examples:**
```
python token_utils.py -t "What is tokenization?" -p 0.0001
python token_utils.py -f messages.json -m gpt-4o-mini -p 0.00015
```

**Test result:**
- "What is tokenization?" → 5 tokens (fallback estimation)
- Cost at $0.0001/1k: $0.000001

**Key lesson:**
- Tiktoken needs internet on first run to download encodings
- Fallback estimation (chars/4) is useful for offline/testing scenarios
- Token counting integrated with .env credentials for consistency

---

## Activity A6: Runtime setup fixes and successful execution
**Status:** Completed

**Outcome:**
- Switched script to load credentials from `.env` via `load_dotenv()`.
- Corrected Azure call to use deployment name from `AZURE_OPENAI_DEPLOYMENT_NAME`.
- Added runtime validation for missing deployment variable with clear error message.
- Confirmed script execution in `.venv` with successful response generation.

**Key lesson:**
- In Azure OpenAI, `model` must be the deployment name, not the base model label.
- Terminal sessions can use different Python interpreters; verify `.venv` path when running.

**Quick checks to remember:**
1. `Get-Command python` should point to `.venv\Scripts\python.exe`.
2. `.env` must include endpoint, API key, API version, and deployment name.
3. If `dotenv` import fails, package is installed in a different interpreter.

---

## Activity A7: Project folder reorganization (post-Day-1 cleanup)
**Status:** Completed  
**Date:** April 17, 2026

**What was organized:**
- Created folder structure: `day_01/`, `docs/`, `shared/`
- Moved all Day 1 files into `day_01/`: DAY_01_NOTES.md, day1_chatbot.py, day1_results.json, token_utils.py
- Moved course documentation into `docs/`: COURSE_DAILY_SCHEDULE.md, ROADMAP_AI_AGENTIC.md, DAILY_CHECKIN_TEMPLATE.md
- Created README.md files for each folder to guide navigation

**Files created:**
- `PROJECT_STRUCTURE.md` (root) — Explains folder organization and how to use each section
- `day_01/README.md` — Quick start guide for Day 1 learning and practice
- `docs/README.md` — Navigation guide for course documentation

**Why this matters:**
- **Scalability:** Easy to add day_02/, day_03/, etc. with same structure
- **Clarity:** Each day is self-contained with notes + code + results
- **Navigation:** README files guide users to the right information quickly
- **Git-friendly:** Clean folder structure makes commits and diffs more meaningful

**Key lesson:**
Project organization is not just for neatness; it enables:
- Easy onboarding (others can quickly understand structure)
- Faster local searching (find what you need in the relevant day folder)
- Better version control (organize commits by day/topic)
- Preparation for scaling (Day 2, 3, ... follow the same pattern)

---

## Activity A8: Created sample_messages.json for token counting practice
**Status:** Completed  
**Date:** April 17, 2026

**What was created:**
- `day_01/sample_messages.json` — A realistic 4-message conversation about tokenization
  - System prompt (behavior instruction)
  - User question #1
  - Assistant response #1
  - User question #2
  - Assistant response #2

**Purpose:**
- Provide a properly formatted messages file for testing `token_utils.py -f` functionality
- Example of what the `-f` (file input) argument expects
- Demonstrate token counting on realistic multi-turn conversations

**Test executed:**
```bash
python token_utils.py -f sample_messages.json -p 0.00015
```

**Result:**
```
Messages tokens: 307
Estimated cost (@0.00015/1k): $0.000046
```

**Why this was needed:**
- Initial error: Tried to pass `day1_results.json` (API response format) instead of messages format
- `token_utils.py -f` expects: `[{"role": "...", "content": "..."}]`
- `day1_results.json` contains: `{"timestamp": "...", "responses": {...}}`
- Fixed by creating a proper messages array file

**Lesson learned:**
File format matters! Always verify:
1. What format does the tool expect?
2. What format do I have?
3. How do I convert between them?

---

# SUMMARY

**Day 1 Complete: All 4 Questions + Full Practice Cycle**

| Q | Topic | Status |
|---|-------|--------|
| Q1 | How OpenAI API works | ✅ |
| Q2 | System prompts | ✅ |
| Q3 | API call structure in Python | ✅ |
| Q4 | Tokenization & cost | ✅ |

**Artifacts created:**
- `day1_chatbot.py` - 3-prompt comparison chatbot (working)
- `day1_results.json` - Saved API responses
- `token_utils.py` - Token counter utility with fallback

**Key takeaways:**
1. Prompt choice is context-dependent; no "best" prompt exists universally.
2. Explicit structure + constraints dramatically improve output quality.
3. Token usage varies by prompt complexity; cost management is critical.
4. Azure OpenAI requires deployment names, not model names, in the model field.
5. API is stateless; you manage conversation history by resending full context.
