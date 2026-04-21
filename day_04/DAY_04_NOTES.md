# Day 4 Learning Notes: Prompt Engineering & Structured Output

Date: April 20, 2026
Course: AI Engineer Core Track

---

## Concept Questions (Q1-Q4)

### Q1: Which few-shot prompting patterns improve structured output consistency?
Your Answer:
Few-shot examples help keep answers in line with user expectations and improve readability. For strict JSON, one example is enough to set the template — this keeps token usage low. Examples should be short and schema-focused so responses stay concise and precise. If the model breaks the format, the fix depends on what is breaking: if the model doesn't understand the expected layout, add more examples; if it understands the intent but drifts on structure, apply output constraints first.

Mentor Notes:
- Score: 4/5 — Correct on all three dimensions; solid diagnostic thinking.
- 1 example is optimal for simple schemas; add a 2nd only when the model misses edge fields. Beyond 3 = diminishing returns + token waste.
- Short + schema-focused is correct: the example *is* the output contract — no prose, no filler.
- Format-break diagnostic: if model understands intent but drifts → output constraints first (faster, cheaper). If model doesn't understand the shape → add a second example.
- Bonus pattern not mentioned: contrasting examples (one correct + one incorrect with annotation) are the most token-efficient way to teach format boundaries when a second example is needed.

### Q2: How should chain-of-thought be used safely for production prompts?
Your Answer:
Chain-of-thought should focus on the goal, the path to reach the goal, and the tasks needed to complete it. Reasoning can be in the same part as the final answer so the answer is explained. If deeper detail is required, it can be separated into another part. The model must be strong enough to meet user-defined validations, otherwise risk is high.

Mentor Notes:
- Score: 3.5/5 - good focus on goal-oriented reasoning and risk awareness.
- Use reasoning only for tasks that require multi-step decisions (planning, tradeoff analysis, debugging), not for every request.
- For production, keep final output separate from any rationale: use explicit fields like `final_answer`, `confidence`, and optional `brief_rationale`.
- Do not validate correctness from reasoning text; validate deterministic fields, schema constraints, and downstream checks.
- Main risk: reasoning can look plausible but still be wrong, inconsistent, or policy-unsafe. Treat it as supporting context, not proof.

### Q3: How do JSON mode and schema constraints improve reliability?
Your Answer:
JSON mode provides structure with key-value pairs that help identify what answers and metrics correspond to what fields. Constraints provide direction and guidance on what the model should think about when answering. If the output has the wrong shape, constraints should catch it first.

Mentor Notes:
- Score: 3.5/5 — Good grasp of JSON structure and constraints as guidance; one key gap on timing.
- JSON mode ensures output is *syntactically parseable* as valid JSON (no curly-brace or quote errors).
- Constraints (in the prompt) are *behavioral guidance*: they steer the model toward the right field names and types before generation.
- But the actual shape validation happens at *runtime in code* via a validator (Pydantic). Constraints prevent errors; validators catch any that slip through.
- Three-layer model: (1) JSON mode = syntax, (2) constraints = guidance, (3) Pydantic = deterministic shape check. All three together are strongest.

### Q4: Why is Pydantic validation critical in production LLM systems?
Your Answer:
Pydantic is like a compiler for output—it catches errors in JSON output even when constraints are applied. Without it, issues can occur. Validation failure should trigger fatal behavior depending on the type of output expected, otherwise automatic retry/repair should handle it. Track deterministic errors from validation failures to understand what causes wrong answers; this data can improve prompts and outputs.

Mentor Notes:
- Score: 4/5 — Excellent metaphor and production-aware thinking on fatal vs retry strategy.
- Pydantic doesn't just catch malformed JSON; it catches silent data corruption. Without it, bad JSON parses silently with wrong types or missing fields.
- Fatal vs retry decision: high-stakes outputs (medical, financial, legal) should fail fast and alert humans. Low-stakes (suggestions, summaries) should retry/repair automatically.
- Error taxonomy tracking is production gold: log field, type, value for every failure. Over time, patterns emerge (e.g., "amounts always come back as strings in field X"). Use that to update your constraints and few-shot examples.
- Feedback loop: validation failure → log error pattern → update prompt/constraints → redeploy. This is how you improve structured output reliability.

---

## Activities (A1-A8)

### A1: Build baseline JSON prompt
Status: ✅ Complete
Evidence: BASELINE_PROMPT_TEMPLATE in day4_structured_output.py (zero-shot JSON generation)
Result: 20/20 test cases produced syntactically valid JSON

### A2: Add few-shot examples for schema adherence
Status: ✅ Complete
Evidence: FEWSHOT_PROMPT_TEMPLATE in day4_structured_output.py (1 schema-focused example)
Result: 20/20 test cases produced valid outputs; no improvement delta needed for strong models

### A3: Build Pydantic model and parse outputs
Status: ✅ Complete
Evidence: TaskAnalysis BaseModel in day4_structured_output.py with field validators, constraints (min_length, max_length, gt, le), and pattern validation (task_id format)
Result: validate_and_parse() function catches all invalid JSON, type mismatches, and constraint violations

### A4: Add retry/repair strategy for invalid responses
Status: ✅ Complete
Evidence: repair_with_retry() function in day4_structured_output.py with max_retries parameter, temperature reduction on subsequent attempts (0.7 → 0.3), and constraint refinement in retry prompt
Result: Ready for production auto-repair of validation failures

### A5: Compare zero-shot vs few-shot validity
Status: ✅ Complete
Evidence: day4_structured_output_report.json A5_comparison section
Result: Baseline (zero-shot) 100.0% (20/20), Few-shot 100.0% (20/20), Improvement +0.0%. Azure model handles schema without examples; prioritize based on token budget.

### A6: Build failure taxonomy and logging
Status: ✅ Complete
Evidence: ValidationFailure dataclass + run_benchmark() tracking in day4_structured_output.py; no failures in benchmark but infrastructure ready
Result: Production-ready logging for field errors, error messages, raw outputs, and prompt types for real-world feedback loop

### A7: Run 20-case validity benchmark
Status: ✅ Complete
Evidence: day4_structured_output_report.json with 20 test cases (mix of simple, edge_case, ambiguous categories)
Result: Baseline 100%, Few-shot 100%; zero failures; zero retries needed. Model strongly handles task analysis schema.

### A8: Final structured-output playbook
Status: ✅ Complete
Evidence: day4_structured_output_report.json A8_playbook section
Result: 8 best practices + 5 next steps for production deployment. Key recommendations: (1) Always use Pydantic, (2) Start with 1 schema-focused example, (3) Log failures for continuous improvement.

---

## Summary
Status: ✅ Complete

All Q1-Q4 concept questions answered and scored. All A1-A8 activities implemented and measured.

**Key Findings:**
- Few-shot prompting improves consistency through schema examples and contrasting patterns.
- Chain-of-thought should be goal-focused and separated from final output; never validate using reasoning text.
- JSON mode + schema constraints work together; Pydantic adds deterministic runtime validation.
- Pydantic is critical: catches silent type corruption and ensures downstream system reliability.
- Structured output benchmark: 100% validity rate on baseline + few-shot with 20 diverse task descriptions.
- Failure-to-feedback loop: track validation errors deterministically to improve prompts over time.

**Artifacts Generated:**
- `day_04/day4_structured_output.py` — Full A1-A8 pipeline (prompts, Pydantic schema, retry/repair, benchmark, playbook)
- `day_04/day4_structured_output_report.json` — Benchmark results and production playbook
