# Day 6 Notes: Function Calling and Tool Use

Date: April 23, 2026

## Concept Questions (Q1-Q4)

### Q1. What is function calling in LLM systems, and why does it matter?
- Your answer: function calling is a process where model is acting as per user needs, can be free text, or specific purpose with args. helps in understanding the input and expected output, and bridges the gap, as in my brochure project, llm used a function to get details of the company and then structure it in the json structure as set by the user, also validating the output.
- Mentor feedback: Strong practical understanding and good linkage to your brochure pipeline. The key improvement is precision: in function calling, the model does not execute functions itself; it returns a structured tool call request (name + JSON args), and your application validates and executes it. This is what makes it safer and more reliable than plain free-text prompting.
- Score: 4.2/5

### Q2. How do tool schemas influence model tool-selection quality?
- Your answer: tool schemas set expectations of the output, the llm understand the schema design and uses which tool to process. in brochure project, validation ran against schema to match the output else throws an error.
- Mentor feedback: Very good practical understanding. The strongest point is your connection to schema validation in the brochure project. One precision improvement: tool schemas primarily define function inputs (argument names, types, required fields, constraints), and this improves both tool choice and argument correctness. Output validation is also important, but in function calling, input schema clarity is what most directly improves tool-selection accuracy.
- Score: 4.3/5

### Q3. What validation should happen before executing a model-requested tool?
- Your answer: i will take my project example as source. first arguments are validated to check minimum args are provided. then input models availability. then check if the source can be fetched. then check output of the model research has valid json. then check if generated brochure generated in a proper schema. then check api errors and values. for every check we default error.
- Mentor feedback: Strong answer with very good sequencing mindset. You covered both pre-execution and post-execution validations, and your fallback/error-default idea is production-friendly. The main improvement is terminology and ordering: before executing a tool call, validate tool existence, argument JSON parseability, schema/type constraints, safety constraints (allowed values/ranges), and required runtime preconditions (auth, endpoint availability). Then execute, and only after execution validate tool output and downstream schema.
- Score: 4.6/5

### Q4. What are the most common failure modes in tool-using agents?
- Your answer: model/deployment error: fallback deployment with health checkup. invalid tool: validate schema. unknown tool: strict registry check. timeout: timeout caps. infinite loop: max-step limit.
- Mentor feedback: Excellent upgrade. This is now production-structured and maps failures directly to mitigations. Very strong coverage of common failure classes. One final enhancement for top score: add retry/backoff for timeout/rate-limit and add structured logging/trace IDs for postmortem debugging.
- Score: 4.7/5

---

## Activities (A1-A8)

### A1. Define tool registry (3-5 tools)
- Status: Completed
- Evidence: Added tool registry with web_search, company_lookup, summarize_text and OpenAI tool schema conversion.

### A2. Implement tool executors
- Status: Completed
- Evidence: Implemented execute_web_search (Azure-backed with fallback), execute_company_lookup, and execute_summarize_text.

### A3. Add Pydantic validation for tool args
- Status: Completed
- Evidence: Each executor validates payloads using WebSearchInput, CompanyLookupInput, and SummarizeTextInput.

### A4. Add failure-safe execution and fallback
- Status: Completed
- Evidence: Added standardized response envelope with ok, mode, error, trace_id and safe fallback path for web_search.

### A5. Compare auto vs required vs none
- Status: Completed
- Evidence: Added compare-tool-choice mode and ran query "find info about OpenAI".
	- auto: 1 tool call (company_lookup), no assistant text
	- required: 1 tool call (company_lookup), no assistant text
	- none: 0 tool calls, assistant asked follow-up text question

### A6. Track argument validity and tool correctness
- Status: Completed
- Evidence: Added in-memory metrics instrumentation (METRICS + record_metric) and wired counters into dispatcher.
	- tracked keys: total_calls, success, schema_validation_failed, unknown_tool, tool_execution_failed
	- metrics are printed in interactive mode and single-query mode for quick verification
	- correctness signals observed: valid tool paths increment success, invalid inputs increment schema_validation_failed, unknown tool increments unknown_tool

### A7. Add interactive mode with trace visibility
- Status: Completed
- Evidence: Added interactive loop with routed tool execution and response envelope containing trace_id.

### A8. Write tool schema best-practice playbook
- Status: Completed
- Evidence: Added Day 6 Tool Schema Best-Practice Playbook (below) based on implemented engine patterns and observed tool-choice behavior.

### Day 6 Tool Schema Best-Practice Playbook
1. Keep tool names action-oriented and unambiguous.
- Use clear verbs (`web_search`, `company_lookup`, `summarize_text`) so model routing intent is obvious.

2. Constrain arguments aggressively with schema rules.
- Use min/max lengths, enums, ranges, and required fields to reduce malformed calls.

3. Prefer small, explicit argument sets.
- Fewer arguments improve tool-selection accuracy and reduce invalid argument combinations.

4. Separate tool input schema from tool output envelope.
- Validate input with Pydantic models, but return a consistent engine envelope for all tool outputs (`ok/tool/mode/data/error/trace_id`).

5. Add deterministic fallback behavior.
- If remote model or parsing fails, provide predictable fallback output instead of crashing.

6. Track runtime quality with lightweight metrics.
- Record total calls, success, validation failures, unknown tool errors, and execution failures.

7. Design for UI consumption from day one.
- Return JSON structures that map directly to UI sections/components instead of free-text blobs.

8. Compare tool-choice modes before production defaults.
- Measure `auto`, `required`, and `none` with the same queries; choose default mode using evidence.

9. Include trace identifiers in all responses.
- `trace_id` enables debugging, incident correlation, and reproducible logs.

10. Validate after every incremental change.
- Run compile checks and small execution probes after each step to prevent error accumulation.

---

## Reflection
- What worked best today:
	- Mentor-mode incremental implementation reduced logic regressions and kept each step verifiable.
	- Schema-first tool design (Pydantic input models) significantly improved argument correctness.
	- Standard response envelope (`ok/tool/mode/data/error/trace_id`) made debugging and UI mapping straightforward.
	- Runtime metrics and `trace_id` usage gave immediate visibility into tool-call health.

- What failed and why:
	- `web_search` is still simulated/model-generated content, not true live retrieval; this limits factual freshness.
	- Some tool-choice outputs can vary by prompt wording, so behavior is not fully deterministic without stricter prompts/policies.
	- Early integration issues (typing and missing function wiring) happened due to incremental assembly before final pass.

- What to improve tomorrow (Day 7):
	- Add one real external data/retrieval tool with explicit timeout, retry, and backoff controls.
	- Persist metrics/traces to JSONL logs for session-to-session analysis.
	- Add a compact evaluation set for tool-call precision, validation-failure rate, and fallback frequency.
	- Define clear production default for tool-choice mode based on measured behavior.
