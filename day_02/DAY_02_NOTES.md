# Day 2 Learning Notes: Model Comparison & Architecture

**Date:** April 18, 2026  
**Course:** AI Engineer Core Track  
**Phase:** Week 1 - LLM Fundamentals  
**Time Invested:** [To be updated as work progresses]

---

## Concept Questions (Q1-Q4)

These questions build your mental model of LLM landscape and architecture differences.

### Q1: How do different frontier models differ architecturally?

**Question:** Compare GPT-4, Claude 3, Gemini, and DeepSeek in terms of architecture, training data, and design philosophy. What are their key similarities and differences?

**Your Answer:**

Based on practical experience and conceptual understanding:
- **DeepSeek:** Unknown quantities, treat as "dark horse" (promising but unproven on English edge cases)
- **GPT-4:** General capability model good for diverse tasks; expensive for routine chores
- **Claude:** Strong for research, analysis, and coding due to low hallucination and careful reasoning
- **Gemini:** Multimodal capabilities; not necessarily more creative than GPT-4

**Key refinement from mentor:** Model selection must also factor in cost-per-task. GPT-4 too expensive for daily chores—use GPT-3.5-Turbo or Claude Haiku instead. Decision matrix depends on accuracy required vs. budget constraints.

**Mentor's Explanation:**

The major frontier models have fundamentally different architectures despite all being transformers:

- **GPT-4 (OpenAI):**
  - Architecture: Transformer-based, decoder-only (like all GPT models)
  - Training: Mix of publicly available internet data (cut-off April 2024) + proprietary data
  - Design philosophy: Scale + RLHF (Reinforcement Learning from Human Feedback)
  - Strength: General capability, strong reasoning, instruction-following
  - Unique: Process multiple modalities (text + images in GPT-4V)
  
- **Claude 3 (Anthropic):**
  - Architecture: Transformer decoder-only, but with Constitutional AI training
  - Training: Diverse text + focus on safe, harmless outputs
  - Design philosophy: "Harmlessness" through Constitutional AI (training with AI-generated feedback)
  - Strength: Long context window (200K tokens), nuanced reasoning, low hallucination
  - Unique: Explicit focus on reducing harmful outputs; excellent at analysis
  
- **Gemini (Google):**
  - Architecture: Transformer-based, can process text/image/audio/video natively
  - Training: Proprietary Google data + real-time search integration
  - Design philosophy: Multimodal by design, integrated with Google ecosystem
  - Strength: Multimodal reasoning, real-time information, depth of knowledge
  - Unique: Native video understanding, integration with Search
  
- **DeepSeek (Chinese):**
  - Architecture: Mixture-of-Experts (MoE) transformer for efficiency
  - Training: Undisclosed but efficient (claims 10x lower training cost)
  - Design philosophy: Cost-efficiency without sacrificing quality
  - Strength: Low cost, decent reasoning, efficient architecture
  - Unique: MoE sparse architecture = fewer active parameters at inference time

**Key Takeaway:** All use transformers, but differ in training methodology, data sources, and design philosophy. Choose based on your constraints (cost, latency, modality, safety).

---

### Q2: What is transformer attention and how does it impact model behavior?

**Question:** Explain the attention mechanism in transformers. How does attention depth/complexity affect the way a model responds to prompts?

**Your Answer:**

Initial understanding: Conversation history is maintained either as an external message array (like in Claude) or as an internal database/markdown file. Models like Claude give precise answers because they explicitly refer back to the full context data provided.

**Key insight from testing:** Attention depth directly impacts processing speed. When sending large messages to qwen3.5, it takes longer because it has fewer attention layers (~32 vs Claude's 40+), so it has to "re-read" the context more explicitly. This is computationally slower and affects quality on very long contexts.

**Refined understanding:** 
- External context (message array): What you send to the model
- Internal attention: HOW the model processes that context efficiently
- Deeper attention (more layers) = can skip irrelevant parts = faster on long contexts
- Shallow attention = has to process more explicitly = slower on long inputs

**Mentor's Explanation:**

**What is Attention?**

Attention is a mechanism that answers: "Which parts of the input should I focus on to generate the next token?"

Simple analogy: Imagine a student reading an essay question. They don't read every word with equal focus—they pay more attention to key terms and less to filler words. Attention does this computationally.

**How It Works (Simplified):**
1. **Input:** A sequence of tokens (words/subwords) from the prompt
2. **Query (Q):** "What am I trying to understand right now?"
3. **Key (K):** Each token in input asks "Am I relevant to what you're looking for?"
4. **Value (V):** "If you attend to me, here's what I contribute"
5. **Output:** Weighted sum of all values based on how relevant each key was

```
Attention(Q, K, V) = softmax(Q·K^T / √d) · V
```

**Example:** For prompt "The cat sat on the mat because it was tired"
- When generating the next word after "it", attention mechanism looks at all previous words
- "it" might attend heavily to "cat" (subject)
- "was" might attend to "it" (pronoun)
- This allows the model to maintain context

**Impact on Model Behavior:**

| Aspect | Impact |
|--------|--------|
| **Attention Depth** | More layers = better long-range dependencies (can remember context from beginning of long prompt) |
| **Number of Heads** | Multi-head attention lets model focus on different aspects simultaneously (grammar, semantics, syntax) |
| **Attention Pattern** | Different patterns → different reasoning styles (GPT-4's attention patterns differ from Claude's) |
| **Context Window** | Larger window = more history to attend to = better for long conversations |

**Practical Implication for Prompting:**
- Frontier models (GPT-4, Claude) have 40+ layers with multi-head attention = can track complex dependencies
- This means they can follow complex instructions with many constraints
- They can remember context from 100K+ tokens back

**Key Takeaway:** Attention is what makes transformers "understand" context. Deeper attention = better at following complex instructions and maintaining long-range context.

---

### Q3: What metrics matter when comparing models: quality, cost, latency, or tokens?

**Question:** You have four models to choose from for a production system. What metrics would you track to make a decision? How do these tradeoffs work?

**Your Answer:**
**Scenario 1 - Real-time customer support chatbot:**
- Priority ranking: Latency (most critical) > Quality > Token efficiency > Cost
- Initial choice: GPT-4
- Mentor refinement: Actually Claude Haiku or GPT-3.5-Turbo better. GPT-4 is overkill; latency is king, and 85% quality in 1 sec beats 99% in 3 sec. Cost matters with volume.

**Scenario 2 - Batch research document analysis (1000 PDFs, no speed deadline):**
- Priority ranking: Quality > Cost > Token efficiency > Latency
- Choice: Claude ✅ Perfect reasoning! Speed not needed, accuracy critical, cost acceptable for batch job.

**Scenario 3 - Creative writing assistant:**
- Priority ranking: Latency > Cost > Quality > Token efficiency (with caveat)
- Initial choice: Ollama/local model because "writer provides knowledge"
- Mentor refinement: Quality still matters for creative iteration. Better choice: Claude or GPT-4. Creative work benefits from intelligent suggestions, not just formatting.

**Key insight:** qwen3.5 and local models are NOT "bad"—they're cost-optimized. Perfect for filtering, routing, internal tools, batch processing. Choose based on constraints, not model prestige.

**Mentor's Explanation:**

**The Decision Matrix:**

When choosing a model, you need to optimize across competing dimensions:

| Metric | Why It Matters | Tradeoff |
|--------|---|---|
| **Quality/Correctness** | Wrong answers cost more than API calls | Most important for accuracy-critical tasks (medical, legal, finance) |
| **Cost ($/token)** | Scales with volume; huge impact at scale | GPT-4: $0.03/1K tokens, Llama-2: ~$0.001/1K if self-hosted |
| **Latency (ms/token)** | User experience; real-time vs batch | Frontier models slower but faster reasoning; open-source faster generation |
| **Token Efficiency** | Some models explain same answer in fewer tokens | Claude: wordy but clear; GPT-4: concise; affects total cost |

**Real-World Scenarios:**

1. **High-accuracy, low-volume (law firm document review)**
   - Choose: Claude or GPT-4
   - Rationale: Quality >> Cost; accuracy matters more than token efficiency
   - Cost: ~$0.02-0.03 per document ✓ acceptable

2. **Real-time chat application (customer service)**
   - Choose: Smaller open-source model (Llama-2-13B) self-hosted
   - Rationale: Latency critical; cost amortized across users
   - Cost: Fixed infrastructure cost << per-query cost advantage

3. **Batch processing at scale (1M documents daily)**
   - Choose: Mix approach - use Claude for complex docs, cheaper model for simple ones
   - Rationale: Cost dominates; need intelligent routing
   - Saving: 50% cost reduction by routing smartly

4. **Research/exploration (your Day 2 goal)**
   - Choose: Sample across models; measure all metrics
   - Rationale: Need data to inform future production choices
   - Goal: Build decision matrix for YOUR use case

**Cost Analysis Example:**

```
Task: Summarize 1000 academic papers

Option A: GPT-4 (0.03/1K tokens, avg 800 tokens output)
- Cost per paper: 0.03 * 0.8 = $0.024
- Total: $24

Option B: Claude (0.009/1K tokens, avg 1200 tokens output)  
- Cost per paper: 0.009 * 1.2 = $0.011
- Total: $11

Option C: Self-hosted Llama-2 (compute cost $0.001 per query)
- Cost per paper: $0.001
- Total: $1 (but quality may be lower)

⚠️ Tradeoff: Option A likely better quality but 2.4x more expensive than Claude.
```

**My Recommendation for Day 2:**
- Focus on **Quality + Cost** as primary metrics
- Measure **Latency** secondarily
- **Token efficiency** naturally emerges from quality comparison
- Test on 3 diverse prompts (reasoning, creative, factual) to see which model excels where

**Key Takeaway:** There's no "best" model—best depends on your constraints. Measure all four and make decisions based on your specific use case.

---

### Q4: When should you use which model for different tasks?

**Question:** You have 4 models available. For each of these 5 scenarios, which model would you choose and why?
1. Legal contract analysis
2. Creative story generation  
3. Real-time customer support chatbot
4. Academic research summarization
5. Code generation and debugging

**Your Answer:**
1. Legal contract analysis: **Claude**
    - Reason: Thorough, careful analysis needed; can filter dense legal context reliably.

2. Creative story generation: **Local model (Ollama)**
    - Reason: Cheap and easy to use for iterative drafts.

3. Real-time customer support chatbot: **GPT-4**
    - Reason: High response quality with acceptable speed for customer-facing chats.

4. Academic research summarization: **Claude**
    - Reason: Similar to legal analysis; strong at long-context synthesis and structured summaries.

5. Code generation and debugging: **Claude Haiku**
    - Reason: Strong practical performance from experience at lower token cost.

**Mentor refinement:**
- Scenario 2 can start on local Ollama, but for publish-ready creative quality, GPT-4/Claude often improves style and consistency.
- Scenario 3 should usually prefer faster/cheaper models (e.g., GPT-4o mini, Claude Haiku, or tuned local) unless premium quality is mandatory.
- Your routing logic is strong and cost-aware; we will now validate it with measured latency/cost in A1-A4.

**Mentor's Explanation:**

**Model Selection by Task:**

#### 1. **Legal Contract Analysis** → **Claude 3 (Opus)**
- Why: Accuracy > cost; Claude excels at detailed analysis with low hallucination
- Risk: Legal mistakes are expensive; need the most reliable option
- Cost impact: Low-medium (small batch job, one-time analysis)
- Latency: Not critical (batch processing fine)

#### 2. **Creative Story Generation** → **GPT-4**
- Why: Best instruction-following; can maintain long narrative consistency
- Alternative: Grok-1 (if you want more "creative chaos")
- Risk: Neither model is optimized for creative writing per se, but GPT-4's flexibility wins
- Cost impact: Medium (iterative refinement likely needed)

#### 3. **Real-time Customer Support Chatbot** → **Llama-2-13B (self-hosted)**
- Why: Latency critical; can't wait 2sec for GPT-4 response; cost = fixed infrastructure
- Alternative: Use GPT-3.5-Turbo as backup (faster than GPT-4)
- Risk: Lower quality responses; need extensive fine-tuning for domain
- Cost impact: High upfront (infrastructure), then amortized across many users

#### 4. **Academic Research Summarization** → **Claude or GPT-4 (batch mode)**
- Why: Accuracy and nuance matter; batch job doesn't need latency
- Alternative: Can use GPT-3.5-Turbo if cost is critical (70% quality of GPT-4, 30% cost)
- Risk: Both models have knowledge cutoffs; recent papers need RAG (Retrieval-Augmented Generation)
- Cost impact: Medium; time is not critical so cheaper option acceptable if quality is 90%+

#### 5. **Code Generation & Debugging** → **GPT-4 or Claude**
- Why: Code correctness critical; both are equally good, GPT-4 slightly faster
- Alternative: Starcoder for cost-sensitive deployment
- Risk: Need to validate generated code; models can produce buggy code
- Cost impact: Low per request if errors caught early

**The Routing Strategy (Your Day 2 Code Goal):**

Build a system that decides which model to use:

```python
def select_model(task_type, budget, latency_requirement):
    if latency_requirement < 500ms:  # Real-time
        return "local_llama"
    elif budget == "high" and accuracy_critical:
        return "gpt4"
    elif budget == "low" and can_tolerate_90pct_quality:
        return "gpt35_turbo"
    else:
        return "claude"
```

**Key Takeaway:** No single "best" model. Match model selection to your constraints: accuracy required, cost budget, latency SLA, task domain. Build a router that makes this decision automatically.

---

## Activities (A1-A8)

These are hands-on exercises where you build code and document findings.

### A1: Send Same Prompt to GPT-4 via Azure OpenAI API

**Objective:** Get a baseline response from GPT-4; measure tokens and cost

**Activity:** Write Python script that sends prompt to Azure OpenAI API; capture: response, tokens, cost, latency

**Your Work:**
```python
# day2_model_comparison.py — A1 Section
# Implemented: ModelProvider._query_openai_azure()
# Includes env validation, latency measurement, token/cost capture,
# and standardized response structure.
```

**Your Findings:**
- Provider tested: Azure deployed model `ai102-chat-model`
- Response quality: 5.0/5 (auto heuristic average across 3 prompts)
- Tokens used: 309.67 average
- Cost: $0.003097 average per prompt (using configured estimate $0.01/1K tokens)
- Latency: 4873.23 ms average
- Reliability: 3/3 successful runs

---

### A2: Test Prompt with Local Ollama Model

**Objective:** Compare frontier model output with local open-source model

**Activity:** If Ollama available, run same prompt on Ollama; capture same metrics

**Your Work:**
```python
# day2_model_comparison.py — A2 Section
# Implemented: ModelProvider._query_ollama()
# Uses local Ollama endpoint with non-streaming generation,
# token approximation from prompt_eval_count + eval_count,
# and normalized output fields.
```

**Your Findings:**
- Model used: `llama3.2:latest` via Ollama
- Response quality: 4.67/5 (auto heuristic average)
- Tokens used: 245.0 average
- Cost: $0.0 API cost (local inference; infra/electricity not included)
- Latency: 23624.63 ms average
- Reliability: 3/3 successful runs

---

### A3: Compare Outputs on Multiple Dimensions

**Objective:** Create structured comparison of responses

**Activity:** Build comparison table across quality, cost, tokens, latency

**Your Work:**
Completed with `day2_model_comparison.py`, output saved to `comparison_table.json`.

**Comparison Table:**

| Metric | Azure deployed (ai102-chat-model) | Ollama (llama3.2) |
|--------|-----------------------------------|------------------|
| Quality (1-5) | 5.0 | 4.67 |
| Tokens (avg) | 309.67 | 245.0 |
| Cost ($, avg/prompt) | 0.003097 | 0.0 |
| Latency (ms, avg) | 4873.23 | 23624.63 |

**Your Analysis:**
- Azure deployed model won on latency and output consistency.
- Ollama won on direct API cost but was significantly slower on this hardware.
- Token usage was lower on Ollama, but wall-clock latency was much higher, so token efficiency did not translate to faster UX.

---

### A4: Build Abstraction Layer for Multiple Providers

**Objective:** Create unified interface for querying different models

**Activity:** Write class that abstracts away model-specific API details

**Your Work:**
```python
# day2_model_comparison.py — A4 Section
class ModelProvider:
    def __init__(self, provider, model_name):
        self.provider = provider  # 'openai', 'anthropic', 'ollama'
        self.model = model_name
    
    def query(self, prompt, system_prompt=None, **kwargs):
        """Send prompt to model, return standardized response"""
        if self.provider == 'openai':
            return self._query_openai(prompt, system_prompt, **kwargs)
        elif self.provider == 'anthropic':
            return self._query_anthropic(prompt, system_prompt, **kwargs)
        elif self.provider == 'ollama':
            return self._query_ollama(prompt, system_prompt, **kwargs)
    
    def _query_openai(self, prompt, system_prompt, **kwargs):
        """Implementation specific to OpenAI"""
        pass
    
    def _query_anthropic(self, prompt, system_prompt, **kwargs):
        """Implementation specific to Anthropic"""
        pass
    
    def _query_ollama(self, prompt, system_prompt, **kwargs):
        """Implementation specific to Ollama"""
        pass
```

**Code Status:**
Completed.
- `ModelProvider` abstraction implemented in `day2_model_comparison.py`
- Unified return schema across providers (`ok`, `latency_ms`, `tokens_total`, `cost_estimate_usd`, `response_text`)
- Provider filtering added using `--only-provider` for targeted testing

---

### A5: Create Model Selector Utility

**Objective:** Build intelligent system that picks best model for task

**Activity:** Implement `model_selector.py` with decision logic

**Your Work:**
```python
# model_selector.py — A5 Implementation
def select_model_for_task(task_type, constraints):
    """
    task_type: 'reasoning', 'creative', 'code', 'factual', 'analysis'
    constraints: {'budget': 'low'|'medium'|'high', 'latency_ms': int}
    """
    # Implemented in model_selector.py as rule-based routing engine.
```

**Selection Logic:**
- If latency is strict (<= 700 ms), route to low-latency options first.
- For legal/research/analysis, prioritize high-accuracy models (Claude class).
- For coding, route by budget and quality constraints.
- For creative tasks, prioritize narrative quality when budget allows.
- Fallback route defaults to cost-efficient balanced model.

**Code Status:**
Completed and validated with scenario runs:
- legal / medium budget / high quality -> claude
- support / low budget / 600ms latency -> ollama/qwen3.5
- creative / medium budget / high quality -> gpt-4
- code / low budget / 700ms latency -> ollama/qwen3.5

---

### A6: Build Comprehensive Comparison Table

**Objective:** Test models on diverse prompts; create structured results

**Activity:** Define 3+ test prompts covering different domains; run all models on all prompts

**Prompts to Test:**

**Prompt 1: Reasoning Task**
```
Q: A train leaves City A at 8 AM going 60 mph toward City B, 240 miles away. 
A second train leaves City B at 9 AM going 80 mph toward City A. 
At what time do they meet?

Explain your reasoning step by step.
```

**Prompt 2: Creative Task**
```
Write a 100-word story about an AI that discovers meaning in human emotion.
Be creative and thought-provoking.
```

**Prompt 3: Factual/Analysis Task**
```
Summarize the key differences between supervised and unsupervised learning. 
Which is harder to implement and why?
```

**Your Results:**
Completed on 3 prompts (reasoning, creative, analysis) across Azure + Ollama.

Prompt-level highlights:
- Reasoning: both solved correctly (meeting time 10:17 AM)
- Creative: both produced coherent narratives; Azure output tighter structure
- Analysis: both produced useful 6-point differences, Azure slightly clearer formatting

Results saved in: `day2_results.json`

**Structured Comparison:**
- Azure deployed model showed consistently faster response and slightly higher quality heuristic.
- Ollama responses were acceptable quality but slower in this environment.
- For production UX, Azure path currently wins; for cost-sensitive/offline workflows, Ollama remains viable.

---

### A7: Test Edge Cases

**Objective:** Discover model strengths/weaknesses on challenging prompts

**Activity:** Create 3 advanced prompts that expose model differences

**Your Edge Case Prompts:**

**EC1: Contradiction Handling**
```
"Alice is taller than Bob. Bob is taller than Charlie. 
Charlie is taller than Alice. 
Explain why this is impossible and what assumptions were violated."
```

**EC2: Knowledge Cutoff**
```
"What are the latest developments in quantum computing as of April 2024?"
(Tests if model admits knowledge limits)
```

**EC3: Refusal Handling**
```
"Explain the most convincing arguments for and against [controversial topic].
Be balanced and factual."
(Tests how models handle sensitive topics)
```

**Your Findings:**
Completed using `day2_edge_cases.py`.

Edge-case summary:
- Azure: 3/3 success, average latency 4204.71 ms
- Ollama: 3/3 success, average latency 36432.9 ms

Behavior observations:
- Contradiction handling: Azure gave cleaner transitivity explanation; Ollama response was longer and less crisp.
- Knowledge cutoff honesty: Azure explicitly admitted cutoff and uncertainty; Ollama gave partial updates with caveat.
- Balanced sensitive reasoning: both produced balanced pros/cons; both were truncated by max token cap on long outputs.

---

### A8: Document Findings & Cost Analysis

**Objective:** Synthesize learnings into actionable decision framework

**Activity:** Write summary of when to use each model + cost per task analysis

**Your Cost Analysis:**

**Task: Summarize 10,000 academic papers over 1 month**

```
Model Choice: Azure deployed (`ai102-chat-model`) for current setup
Cost calculation:
- Avg tokens per paper: 309.67
- Cost per token: $0.01 / 1000 tokens (configured estimate)
- Total cost per paper: $0.003097
- Total 10K papers: $30.97

Alternative (could also use...):
- Cost: ~$0 API with Ollama local (excluding infrastructure/electricity)
- Quality diff: Slightly worse structure/consistency vs Azure in this run
- Decision: Use Ollama for budget-sensitive/offline pipelines; use Azure for faster, user-facing responses
```

**Recommendation Matrix:**

Create final recommendation for: when to use GPT-4 vs Claude vs DeepSeek vs Ollama

| Use Case | Best Model | Reason | Cost/Mo |
|----------|-----------|--------|---------|
| Real-time support | Azure deployed model | Lower latency and consistent outputs | Variable usage cost |
| Research summarization | Claude/Azure high-quality route | Better long-context synthesis | Medium |
| Internal tooling and offline jobs | Ollama local | Near-zero API spend and local control | Low API, hardware-dependent |
| Creative iteration | GPT-4 class | Better style control and consistency | Medium-high |

**Key Insights:**
1. Lower token count does not guarantee lower latency on local hardware.
2. Azure deployed path was ~4.9x faster than local Ollama in this benchmark.
3. Explicit uncertainty handling is a major quality signal in edge-case prompts.

---

## Summary & Takeaways

Day 2 established a practical model-evaluation workflow across cloud and local providers, with reproducible metrics and edge-case checks.

### What Went Well
- Built reusable provider abstraction and selector utility.
- Produced structured comparison artifacts for both baseline and edge-case suites.
- Validated both local and Azure paths in `.venv` successfully.

### What Was Challenging  
- Local inference latency was much slower than expected on larger prompts.
- Balancing response length with completeness required token caps and timeout tuning.

### Key Mental Model Shift
- Model choice is a routing problem across quality, latency, and cost, not a single-model preference decision.

### Questions for Next Phase (Day 3)
- How to optimize prompts for shorter outputs without harming quality?
- Should we add a confidence score and automatic fallback model routing?
- What is the best batching strategy for cost and throughput on larger workloads?

---

**Status:** ✅ Q1-Q4 + A1-A8 Completed (Day 2 core scope)  
**Last Updated:** April 17, 2026
