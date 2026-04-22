# Day 5 Notes: Agentic Patterns & Tool Use

Date: April 21, 2026
Status: In Progress

## Q1: What is ReAct and when is it better than CoT alone?
- Draft answer: "when we want intuitive answers, or adaptive answers, then react becomes helpful"
- Mentor score: 3.5/5
- Evidence:
	- Strength: Identified adaptiveness as the key value of ReAct.
	- Gap: ReAct should be framed as tool-grounded reasoning for external facts and multi-step workflows.
	- Refined answer:
		- ReAct is better when tasks need external evidence (database/API/search), not only internal reasoning.
		- ReAct is better for multi-step flows where each next action depends on prior observations.
		- ReAct reduces hallucinations by grounding intermediate steps in tool outputs.
		- ReAct improves production debugging with explicit action/observation traces.
		- ReAct is ideal when retry/repair behavior is needed after failed tool calls.
	- Example: Check user status in DB, then send conditional email if overdue.

## Q2: How should tool definitions be designed?
- Draft answer: "tool definition must have proper name and description,easy for the user to identify its purpose. use less ambiguous names such that user doesnt get confused"
- Mentor score: 3.5/5
- Evidence:
	- Strength: Correctly emphasized clear naming and explicit purpose.
	- Gap: Missing schema strictness, constraints, output format, and error contracts.
	- Refined answer:
		- Every tool should define: name, purpose, required inputs, optional inputs, and output shape.
		- Input schemas should be strict (types, ranges, enums, length limits) to prevent bad calls.
		- Tool responsibilities should be narrow and single-purpose to reduce ambiguity.
		- Include clear failure format (error_code/message) so the agent can retry or fallback.
		- Use examples of valid calls for edge cases to improve model call accuracy.
	- Common mistake: generic tool names like "process" or "handle_data" that hide intent and cause wrong routing.

## Q3: What goes wrong in multi-step loops?
- Draft answer: "infinite calls between agents for a requirement; context was not shared among agent and I had to re-apply definitions while switching systems; contradicting decisions among agents; need stronger rules/constraints; plus cost and latency"
- Mentor score: 4.5/5
- Evidence:
	- Strength: Identified the most important production failures from real experience (looping, context loss, contradictory outputs, and cost/latency drift).
	- Gap: Add measurable controls and explicit stop/retry policies.
	- Refined answer:
		- Infinite or long loops happen when no clear stop condition, confidence threshold, or max-step budget is defined.
		- Context fragmentation causes repeated work when agent handoff schema/memory is inconsistent.
		- Contradictory decisions occur when roles and authority boundaries are unclear.
		- Tool misuse appears when validation is weak (wrong tool, wrong params, stale observations).
		- Cost and latency spike when retry/fallback strategy is unconstrained.
	- Control recommendations:
		- Set max iterations and explicit exit criteria per task.
		- Use a strict shared state schema for all handoffs.
		- Define role-level decision rights and conflict resolution rules.
		- Track loop depth, retry count, and tool error rate with alerts.

## Q4: How do you measure and improve agentic success rates?
- Draft answer: "track output metrics like temperature, token count, validity; track input/output token usage across agents to reduce cost; validate data between agents; track outcome success rate"
- Mentor score: 4.0/5
- Evidence:
	- Strength: Correctly selected the core production metrics (success, validity, and token/cost).
	- Gap: Add latency, retry depth, hallucination rate, and a closed-loop improvement process.
	- Refined answer:
		- Track outcome metrics: task success rate, first-pass success rate, and human override rate.
		- Track quality metrics: schema validity, factuality checks, and cross-agent consistency rate.
		- Track efficiency metrics: input/output tokens, cost per successful task, P95 latency, and average loop depth.
		- Track reliability metrics: tool error rate, retry rate, hallucinated tool-call rate, and timeout rate.
		- Improve with a feedback loop: analyze top failure clusters weekly, tighten schemas/prompts, and run A/B benchmarks before rollout.
	- Production targets example:
		- Success >= 85%, schema validity >= 95%, hallucinated tool calls <= 2%, and cost per success trending down week over week.

---

## A1-A8 Tracking

### A1: Tool registry with 5 sample tools
Status: Complete
Evidence: day5_agentic_react.py build_tool_registry()

### A2: ReAct loop implementation
Status: Complete
Evidence: run_react_agent() with thought/action/observation traces

### A3: Tool schema validation
Status: Complete
Evidence: Pydantic models for each tool input

### A4: Retry/repair for failed tool calls
Status: Complete
Evidence: repair_params() and one-step retry on tool failure

### A5: 15-case benchmark
Status: Complete
Evidence: BENCHMARK_CASES and run_benchmark()

### A6: Hallucination pattern tracking
Status: Complete
Evidence: hallucinated_calls metric and fallback behavior

### A7: Success/token/loop metrics
Status: Complete
Evidence: aggregate_report() summary section

### A8: Agentic playbook
Status: Complete
Evidence: report playbook section in output JSON

---

## Reflection
- What worked well:
- What failed:
- Next iteration:
