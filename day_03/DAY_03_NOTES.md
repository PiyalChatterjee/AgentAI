# Day 3 Learning Notes: Tokenization and Cost Optimization

Date: April 20, 2026
Course: AI Engineer Core Track

---

## Concept Questions (Q1-Q4)

### Q1: How does tokenization work in modern LLMs?

**Your Answer:**
Tokens are most likely words in context, not necessarily literal words but groups of words that make a context. LLMs need context to understand what to process, so tokens become more important than individual letters.

**Mentor Refinement:**
You got the key insight right: context matters more than letters. The precise refinement is that tokens are **subword units** — smaller than words but larger than characters — the sweet spot between too granular (letters) and too large (full words).

**BPE (Byte Pair Encoding):**
- Start with all characters, repeatedly merge the most frequent pairs
- Common words stay whole ("cat" = 1 token)
- Rare/long words split into known parts ("tokenization" = ["token", "ization"] = 2 tokens)
- Target vocabulary size: ~50,000 tokens for GPT models

**Practical examples:**
```
"What is tokenization?" = ["What", " is", " token", "ization", "?"] = 5 tokens (not 4 words)
"2024"                  = ["2", "0", "2", "4"] = 4 tokens (each digit separate!)
"AI"                    = ["AI"] = 1 token (common abbreviation)
```

**Why subwords and not full words?**
- Whole-word vocabulary would be millions of entries (every language, typo, rare term)
- Subwords handle unknown words by splitting them into known parts
- English text: ~1 token per word; code and numbers: more tokens per character

**Key Takeaway:** Every token = compute + cost. Understanding token boundaries helps you write cheaper and faster prompts.

### Q2: Why do tokens affect both cost and latency?

**Your Answer:**
More tokens means more work for the LLM to analyse, so more compute effort is spent. When token count approaches the context limit, analysis slows down significantly. Input and output tokens are different processes: input is for understanding the prompt, output is for generating the result — so they are priced and processed differently.

**Mentor Refinement:**
- Output tokens are ~3x more expensive than input tokens because generation is autoregressive (sequential, one token at a time) vs input processing which is parallelized.
- Attention scales O(n²) with context size — doubling tokens quadruples computation, explaining the dramatic slowdown near context limits observed in Day 2 Ollama runs.
- Key optimization implication: reducing output length saves 3x more money than reducing input length.

**Mentor Notes:**
- Every token requires one forward pass through all attention layers — more tokens = more compute.
- Prompt tokens (input) are charged at input rate; completion tokens (output) at output rate — often 2-3x more expensive.
- Latency has two components: time-to-first-token (TTFT) and time-to-last-token (total); both grow with token count.
- Context window fills from left: the closer you are to the limit, the slower and costlier each call becomes.

**Cost formula:**
```
Total cost = (prompt_tokens × price_input_per_1K) + (completion_tokens × price_output_per_1K)
```

**Day 2 evidence:** Azure avg tokens 309.67 at $0.01/1K = $0.003097/prompt. At 1 million daily calls that's $3,097/day — token efficiency directly changes your infrastructure budget.

### Q3: What are practical token optimization techniques?

**Your Answer:**
1. Lead with role/context in the first line — model immediately knows what it's performing
2. Make prompts precise — less vague language means fewer input tokens
3. Set max_tokens and temperature — hard cap output length; lower temperature produces more concise targeted responses

**Mentor Refinement:**
- Tactic 1: Crisp system prompt saves 40-70 tokens on every single API call (paid every call, compounds at scale)
- Tactic 2: Add explicit output constraints in the prompt itself ("3 bullets, max 12 words each") — controls completion token count which saves 3x vs input savings
- Tactic 3: temperature=0.1-0.3 + max_tokens is the production combination for cost-efficient, consistent outputs
- Tactic 4 (missed): Conversation history pruning — resending full history every turn is the biggest hidden token cost; keep only last N turns + summary of older context

**Mentor Notes:**

| Technique | How | Token saving |  
|-----------|-----|-------------|
| Trim system prompt | Remove filler words, keep only constraints | 20-40% |
| Constrain output format | "Reply in 3 bullets max 10 words each" | 30-50% |
| Drop stale history | Remove oldest turns when context >50% full | 20-60% |
| Few-shot pruning | Keep only 1 example instead of 3 if quality holds | 10-30% |
| Batch similar requests | Group prompts to share system prompt cost | Per-call savings |
| Use cheaper model for routing | Let small model classify task, only escalate to large | 70%+ cost reduction |

**Rule of thumb:** System prompt is paid on every API call. A 500-token system prompt at $0.01/1K tokens on 1M daily calls = $5,000/day just for the prompt.

### Q4: How do you keep quality while reducing tokens?

**Your Answer:**
1. History helps quality — if last answer broke code, providing that historical context helps LLM produce better corrections
2. Cutting tokens can improve quality if we remove unnecessary data — model focuses on what matters rather than being distracted
3. If output is missing key constraints, that's how you know optimization broke quality

**Mentor Refinement:**
- Tactic 1 = **targeted context**: keep only causally relevant history turns, not all history. Turn 5 caused the bug + turn 10 is current ask = 150 tokens vs 800 for full history.
- Tactic 2 = **signal-to-noise ratio**: bloated prompts with redundant examples/filler actually confuse models. Cleaner prompts often produce more accurate outputs.
- Tactic 3 = **regression testing**: define upfront what output MUST contain (key fields, format, facts). After optimization, run the same test prompts and check those requirements are still met.

**The sweet spot model:**
```
Too few tokens:  model lacks context → wrong/incomplete output
Just right:      minimum viable context → fast, cheap, accurate
Too many tokens: model distracted by noise → slower, costlier, sometimes worse
```

**Key Takeaway:** Always test-measure-compare. Never optimize blindly. Keep a fixed test set and run it before and after every change.

**Mentor Notes:**
- Optimization without measurement is guessing. Always run the same 3-5 fixed test prompts before and after.
- Quality signals to track: output format compliance, factual correctness, completeness of answer.
- Safe optimizations first: trim whitespace/filler, cut redundant instructions.
- Risky optimizations second (measure carefully): reduce examples, shorten constraints, drop history.
- Stop optimizing when quality drops below your acceptable threshold — not before.

**The test-measure loop:**
```
1. Establish baseline (token count + quality score)
2. Apply one optimization
3. Re-run fixed test set
4. Compare quality score
5. Keep if quality ≥ threshold AND tokens reduced
6. Revert if quality drops
```

---

## Activities (A1-A8)

### A1: Baseline token benchmark
Status: Completed ✅

Results:
- Baseline prompt tokens (avg across 3 roles): 84.67
- Baseline estimated cost/call: $0.007447

### A2: Prompt rewrite and compression
Status: Completed ✅

Results:
- Optimized prompt tokens (avg): 43.33
- Prompt token reduction: 48.82%
- Cost reduction (estimated): 45.84%
- Redundancy insight: Friendly-teacher baseline had the most redundant text, product-manager next, and technical-expert least, which matched prompt-token and cost differences.

### A3: Token budget checker utility
Status: Completed ✅

Results:
- Implemented budget checker with context usage status (`safe`/`warning`/`risk`)
- All optimized cases stayed in `safe` zone (< 50% context usage)

### A4: Response-length controls
Status: Completed ✅

Results:
- Baseline max completion tokens: 220
- Optimized max completion tokens: 120
- Guardrails added: temperature=0.2, top_p=0.9, explicit quality gate

### A5: Cost estimator for batch usage
Status: Completed ✅

Results:
- Projection @ 1,000,000 calls/day:
	- Baseline daily: $7,446.67
	- Optimized daily: $4,033.33
	- Daily savings: $3,413.33
	- Monthly savings: $102,400.00

### A6: Compare cost curves by model
Status: Completed ✅

Results:
- Added model-profile cost curves in `day3_cost_report.json`:
	- azure_deployed_current: $0.007457 -> $0.004043 (45.78%), monthly savings $102,400.00
	- gpt_4o_mini_like: $0.001449 -> $0.000786 (45.70%), monthly savings $19,860.00
	- premium_frontier_like: $0.007457 -> $0.004043 (45.78%), monthly savings $102,400.00

Takeaway:
- Relative savings percentage stays similar across profiles, but absolute savings depends heavily on model pricing tier.

### A7: Quality regression checks under token caps
Status: Completed ✅

Results:
- Added token-cap risk checks for caps 80/100/120/160 per prompt family.
- Risk outcomes across all three cases:
	- 80: high risk
	- 100: high risk
	- 120: medium risk
	- 160: low risk
- Recommended completion floor: 120 tokens for current 8-bullet constraints.

### A8: Final optimization playbook
Status: Completed ✅

Results:
- Auto-generated playbook now included in `day3_cost_report.json`:
	- Principles: prompt compression, output-cap optimization with quality gates, model routing, targeted history
	- Measured wins: 48.25% prompt reduction, 45.78% cost reduction
	- Defaults: temperature=0.2, top_p=0.9, max_tokens=120
	- Best-savings profile from current run: azure_deployed_current

---

## Summary
Status: In Progress

Current Day 3 progress:
- Q1-Q4 completed
- A1-A8 completed with measurable savings and regression guidance

Artifacts:
- `day_03/day3_token_optimization.py`
- `day_03/day3_cost_report.json`
