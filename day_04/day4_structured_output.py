#!/usr/bin/env python3
"""
Day 4: Structured Output & JSON Validation Pipeline
Activities A1-A8: Few-shot, Pydantic, retry/repair, and validity benchmarking.

A1: Baseline JSON prompt (zero-shot)
A2: Add few-shot examples for schema adherence
A3: Build Pydantic model and parser
A4: Add retry/repair strategy for invalid responses
A5: Compare zero-shot vs few-shot validity rates
A6: Build failure taxonomy and logging
A7: Run 20-case validity benchmark
A8: Generate structured-output playbook with best practices
"""

import json
import argparse
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
from enum import Enum

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator

# Load environment
load_dotenv()

# ============================================================================
# A3: PYDANTIC SCHEMA - Define strict output structure
# ============================================================================

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskAnalysis(BaseModel):
    """
    Structured task analysis with validation.
    The model enforces types, required fields, and pattern matching.
    """
    task_id: str = Field(..., description="Unique identifier for the task")
    description: str = Field(..., min_length=5, max_length=500)
    priority: TaskPriority = Field(..., description="One of: low, medium, high, critical")
    estimated_hours: float = Field(..., gt=0, le=160)
    owner: str = Field(..., min_length=2, max_length=100)
    risk_factors: List[str] = Field(default_factory=list, max_length=5)
    success_criteria: str = Field(..., min_length=10, max_length=200)
    
    @field_validator('task_id')
    @classmethod
    def task_id_format(cls, v):
        if not v.startswith('TASK-'):
            raise ValueError('task_id must start with TASK-')
        return v


# ============================================================================
# A1 & A2: TEST CASES - 20 realistic task descriptions for structured output
# ============================================================================

@dataclass
class TestCase:
    case_id: int
    input_description: str
    expected_priority: str
    expected_owner: str
    category: str  # For grouping (simple, edge_case, ambiguous)


TEST_CASES = [
    TestCase(1, "Fix critical database connection timeout in production affecting 10k users", "critical", "DevOps", "simple"),
    TestCase(2, "Update documentation for new API endpoints", "low", "Documentation", "simple"),
    TestCase(3, "Investigate intermittent 500 errors in payment processing", "high", "Backend", "ambiguous"),
    TestCase(4, "Code review for new authentication module", "medium", "Security", "simple"),
    TestCase(5, "Refactor legacy authentication service to modern standards", "high", "Backend", "simple"),
    TestCase(6, "Add unit tests to discount calculation module", "medium", "QA", "simple"),
    TestCase(7, "Urgent: Deploy security patch for XSS vulnerability", "critical", "Security", "simple"),
    TestCase(8, "Optimize slow customer dashboard query", "medium", "Backend", "edge_case"),
    TestCase(9, "Plan migration to new data warehouse", "high", "Data", "ambiguous"),
    TestCase(10, "Fix typo in user error message", "low", "Frontend", "simple"),
    TestCase(11, "Investigate memory leak reported by customers", "critical", "DevOps", "edge_case"),
    TestCase(12, "Design new metrics dashboard for real-time monitoring", "medium", "Data", "ambiguous"),
    TestCase(13, "Update SSL certificate before expiration next month", "high", "DevOps", "simple"),
    TestCase(14, "Implement role-based access control for admin panel", "high", "Backend", "simple"),
    TestCase(15, "Fix broken email notifications in staging", "low", "QA", "simple"),
    TestCase(16, "Audit and close all open security findings", "critical", "Security", "simple"),
    TestCase(17, "Improve API response time from 2s to 200ms", "high", "Backend", "ambiguous"),
    TestCase(18, "Migrate 500k users to new authentication provider", "critical", "Backend", "edge_case"),
    TestCase(19, "Write integration tests for payment gateway", "medium", "QA", "simple"),
    TestCase(20, "Research and recommend caching strategy for high-traffic endpoints", "medium", "Architecture", "ambiguous"),
]


# ============================================================================
# PROMPTS - A1: BASELINE (ZERO-SHOT), A2: FEW-SHOT
# ============================================================================

BASELINE_PROMPT_TEMPLATE = """You are a task analysis expert. Analyze the following task description and output ONLY valid JSON matching this exact schema:

{{
    "task_id": "TASK-XXXXX",
    "description": "concise description",
    "priority": "low|medium|high|critical",
    "estimated_hours": number,
    "owner": "team name",
    "risk_factors": ["factor1", "factor2"],
    "success_criteria": "how to measure success"
}}

Task: {task_description}

Output ONLY the JSON object, nothing else."""

FEWSHOT_PROMPT_TEMPLATE = """You are a task analysis expert. Analyze task descriptions and output ONLY valid JSON. Here is one example:

Example:
Task: Urgent: Resolve production database outage affecting checkout flow
{{
    "task_id": "TASK-00001",
    "description": "Resolve production database outage affecting checkout flow",
    "priority": "critical",
    "estimated_hours": 4.0,
    "owner": "DevOps",
    "risk_factors": ["customer trust", "revenue impact"],
    "success_criteria": "Customers can check out successfully within 5 minutes"
}}

Now analyze this task. Output ONLY the JSON object, nothing else:

Task: {task_description}

Output ONLY the JSON object:"""


# ============================================================================
# A6: FAILURE TAXONOMY - Track validation errors deterministically
# ============================================================================

@dataclass
class ValidationFailure:
    case_id: int
    field: str
    error_message: str
    raw_output: str
    prompt_type: str  # "baseline" or "fewshot"


# ============================================================================
# AZURE OPENAI CLIENT
# ============================================================================

def call_azure_openai(prompt: str, model: str = None, temperature: float = 0.7, max_tokens: int = 500) -> str:
    """Call Azure OpenAI deployment and return response text."""
    if model is None:
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
    
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-01")
    
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }
    
    url = f"{endpoint}/openai/deployments/{model}/chat/completions?api-version={api_version}"
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that outputs valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()


# ============================================================================
# A3 & A4: PYDANTIC VALIDATION & REPAIR
# ============================================================================

def validate_and_parse(raw_json_str: str) -> tuple[Optional[TaskAnalysis], Optional[str]]:
    """
    A3: Parse and validate JSON against Pydantic schema.
    Returns (parsed_object, error_message) or (None, error_message) if invalid.
    """
    try:
        # Try to extract JSON from response (model might add extra text)
        if "```json" in raw_json_str:
            raw_json_str = raw_json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_json_str:
            raw_json_str = raw_json_str.split("```")[1].split("```")[0].strip()
        
        data = json.loads(raw_json_str)
        task = TaskAnalysis(**data)
        return task, None
    except json.JSONDecodeError as e:
        return None, f"json_parse_error: {str(e)}"
    except ValidationError as e:
        # Extract first field error for taxonomy
        first_error = e.errors()[0]
        field = first_error['loc'][0] if first_error['loc'] else 'unknown'
        msg = first_error['msg']
        return None, f"validation_error:{field}:{msg}"
    except Exception as e:
        return None, f"unexpected_error: {str(e)}"


def repair_with_retry(case: TestCase, prompt_type: str, max_retries: int = 2) -> tuple[Optional[TaskAnalysis], int, Optional[ValidationFailure]]:
    """
    A4: Implement retry/repair strategy.
    On validation failure, refine the constraint and retry up to max_retries times.
    Returns (parsed_task, attempt_number, validation_failure_or_none)
    """
    for attempt in range(max_retries + 1):
        try:
            if prompt_type == "baseline":
                prompt = BASELINE_PROMPT_TEMPLATE.format(task_description=case.input_description)
            else:
                prompt = FEWSHOT_PROMPT_TEMPLATE.format(task_description=case.input_description)
            
            # Add stricter guidance on retries
            if attempt > 0:
                prompt += f"\n\nIMPORTANT (attempt {attempt + 1}): Ensure task_id starts with TASK-, priority is one of [low, medium, high, critical], and estimated_hours is a number between 0.5 and 160."
            
            raw_response = call_azure_openai(prompt, temperature=0.3 if attempt > 0 else 0.7)
            task, error = validate_and_parse(raw_response)
            
            if task is not None:
                return task, attempt + 1, None
            else:
                # Track failure for taxonomy
                if attempt == max_retries:
                    failure = ValidationFailure(
                        case_id=case.case_id,
                        field=error.split(":")[1] if ":" in error else "unknown",
                        error_message=error,
                        raw_output=raw_response[:200],  # Truncate for storage
                        prompt_type=prompt_type
                    )
                    return None, attempt + 1, failure
        except Exception as e:
            if attempt == max_retries:
                failure = ValidationFailure(
                    case_id=case.case_id,
                    field="api_error",
                    error_message=str(e),
                    raw_output="",
                    prompt_type=prompt_type
                )
                return None, attempt + 1, failure
    
    return None, max_retries + 1, None


# ============================================================================
# A7: BENCHMARK - Run all 20 cases and measure validity
# ============================================================================

@dataclass
class BenchmarkResult:
    prompt_type: str  # "baseline" or "fewshot"
    total_cases: int
    valid_outputs: int
    invalid_outputs: int
    validity_rate: float
    avg_attempts: float
    failures: List[ValidationFailure]


def run_benchmark(max_retries: int = 2) -> tuple[BenchmarkResult, BenchmarkResult]:
    """
    A5, A6, A7: Run 20 test cases against both baseline and few-shot prompts.
    Track failures, measure validity rates, and compare.
    """
    baseline_results = []
    fewshot_results = []
    baseline_failures = []
    fewshot_failures = []
    
    print(f"\n{'='*70}")
    print("A7: RUNNING 20-CASE VALIDITY BENCHMARK")
    print(f"{'='*70}")
    
    for case in TEST_CASES:
        print(f"\n[Case {case.case_id}] {case.input_description[:50]}...")
        
        # Baseline (zero-shot)
        print("  → Testing baseline (zero-shot)...", end=" ")
        task_baseline, attempts_baseline, failure_baseline = repair_with_retry(case, "baseline", max_retries)
        is_valid_baseline = task_baseline is not None
        baseline_results.append(is_valid_baseline)
        if failure_baseline:
            baseline_failures.append(failure_baseline)
        print(f"{'✓' if is_valid_baseline else '✗'} ({attempts_baseline} attempts)")
        
        # Few-shot
        print("  → Testing few-shot (with example)...", end=" ")
        task_fewshot, attempts_fewshot, failure_fewshot = repair_with_retry(case, "fewshot", max_retries)
        is_valid_fewshot = task_fewshot is not None
        fewshot_results.append(is_valid_fewshot)
        if failure_fewshot:
            fewshot_failures.append(failure_fewshot)
        print(f"{'✓' if is_valid_fewshot else '✗'} ({attempts_fewshot} attempts)")
    
    # Compute aggregates
    baseline_valid = sum(baseline_results)
    fewshot_valid = sum(fewshot_results)
    
    baseline_result = BenchmarkResult(
        prompt_type="baseline",
        total_cases=len(TEST_CASES),
        valid_outputs=baseline_valid,
        invalid_outputs=len(TEST_CASES) - baseline_valid,
        validity_rate=baseline_valid / len(TEST_CASES) * 100,
        avg_attempts=0,  # Would need to track per-case
        failures=baseline_failures
    )
    
    fewshot_result = BenchmarkResult(
        prompt_type="fewshot",
        total_cases=len(TEST_CASES),
        valid_outputs=fewshot_valid,
        invalid_outputs=len(TEST_CASES) - fewshot_valid,
        validity_rate=fewshot_valid / len(TEST_CASES) * 100,
        avg_attempts=0,
        failures=fewshot_failures
    )
    
    return baseline_result, fewshot_result


# ============================================================================
# A8: PLAYBOOK - Generate structured-output best practices
# ============================================================================

def build_playbook(baseline: BenchmarkResult, fewshot: BenchmarkResult) -> dict:
    """
    A8: Generate production playbook with recommendations based on benchmark results.
    """
    improvement = fewshot.validity_rate - baseline.validity_rate
    
    # Build failure taxonomy insights
    failure_types = {}
    for f in baseline.failures + fewshot.failures:
        field = f.field
        if field not in failure_types:
            failure_types[field] = 0
        failure_types[field] += 1
    
    most_common_failures = sorted(failure_types.items(), key=lambda x: x[1], reverse=True)[:3]
    
    playbook = {
        "title": "Day 4 Structured Output Playbook",
        "timestamp": datetime.now().isoformat(),
        "executive_summary": {
            "baseline_validity": f"{baseline.validity_rate:.1f}%",
            "fewshot_validity": f"{fewshot.validity_rate:.1f}%",
            "improvement_delta": f"{improvement:+.1f}%",
            "recommendation": "Use few-shot prompting" if improvement > 5 else "Both approaches comparable; choose based on token budget"
        },
        "failure_taxonomy": {
            "most_common_failures": [{"field": f[0], "count": f[1]} for f in most_common_failures],
            "total_failures": len(baseline.failures) + len(fewshot.failures)
        },
        "best_practices": [
            "1. Always use Pydantic for validation—silent corruption is worse than loud failure.",
            "2. For structured output, start with one short schema-focused example (few-shot).",
            "3. If validation fails, prioritize output constraints; only add more examples if model doesn't understand the schema.",
            "4. Log all validation failures (field, error type, raw output) to build a feedback loop.",
            "5. Use retry/repair with lower temperature on subsequent attempts—model is more deterministic when correcting.",
            "6. For critical outputs (payments, legal), fail fast and alert humans. For suggestions, auto-repair is acceptable.",
            "7. Monitor failure patterns weekly. If task_id format breaks >2x, add explicit regex constraint in prompt.",
            "8. Track three metrics: validity_rate (% of valid JSON), parse_rate (% of syntactically correct JSON), and repair_success_rate (% recovered by retry)."
        ],
        "next_steps": [
            "Deploy baseline + few-shot variant to production with feature flag.",
            "Collect real-world validation failures for 1 week.",
            "Use failure taxonomy to refine constraints and examples.",
            "Measure improvement in production validity rate.",
            "Document which failure types are highest priority to fix."
        ]
    }
    
    return playbook


# ============================================================================
# MAIN: Orchestrate A1-A8
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Day 4: Structured Output & JSON Validation")
    parser.add_argument("--model", default=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini"), help="Azure OpenAI deployment name")
    parser.add_argument("--max-retries", type=int, default=2, help="Max retry attempts per case")
    parser.add_argument("--out", default="day4_structured_output_report.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    print(f"\n{'='*70}")
    print("DAY 4: STRUCTURED OUTPUT & JSON VALIDATION PIPELINE")
    print(f"{'='*70}")
    print(f"Model: {args.model}")
    print(f"Max retries per case: {args.max_retries}")
    print(f"Output file: {args.out}")
    
    # A1-A2: Define prompts (above)
    print("\n✓ A1: Baseline prompt defined (zero-shot)")
    print("✓ A2: Few-shot prompt with schema example defined")
    
    # A3-A4: Pydantic + Repair (used in benchmark)
    print("✓ A3: Pydantic TaskAnalysis schema defined with validation rules")
    print("✓ A4: Retry/repair strategy implemented (temperature adjustment + constraint refinement)")
    
    # A5-A7: Run benchmark
    baseline_result, fewshot_result = run_benchmark(max_retries=args.max_retries)
    
    # A5: Compare
    print(f"\n{'='*70}")
    print("A5: ZERO-SHOT VS FEW-SHOT COMPARISON")
    print(f"{'='*70}")
    print(f"Baseline (zero-shot):  {baseline_result.valid_outputs}/{baseline_result.total_cases} valid ({baseline_result.validity_rate:.1f}%)")
    print(f"Few-shot (w/ example): {fewshot_result.valid_outputs}/{fewshot_result.total_cases} valid ({fewshot_result.validity_rate:.1f}%)")
    print(f"Improvement:           {fewshot_result.validity_rate - baseline_result.validity_rate:+.1f}%")
    
    # A6: Failure taxonomy
    print(f"\n{'='*70}")
    print("A6: FAILURE TAXONOMY")
    print(f"{'='*70}")
    all_failures = baseline_result.failures + fewshot_result.failures
    if all_failures:
        failure_fields = {}
        for f in all_failures:
            key = f"{f.field}:{f.prompt_type}"
            if key not in failure_fields:
                failure_fields[key] = 0
            failure_fields[key] += 1
        print(f"Total failures: {len(all_failures)}")
        for field_key, count in sorted(failure_fields.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {field_key}: {count}")
    else:
        print("No failures recorded!")
    
    # A8: Playbook
    playbook = build_playbook(baseline_result, fewshot_result)
    
    print(f"\n{'='*70}")
    print("A8: STRUCTURED OUTPUT PLAYBOOK")
    print(f"{'='*70}")
    print(f"\nRecommendation: {playbook['executive_summary']['recommendation']}")
    print("\nBest Practices:")
    for practice in playbook['best_practices'][:3]:
        print(f"  • {practice}")
    
    # Save artifact
    artifact = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "model": args.model,
            "total_test_cases": len(TEST_CASES),
            "max_retries": args.max_retries
        },
        "A5_comparison": {
            "baseline": asdict(baseline_result) | {"failures": [asdict(f) for f in baseline_result.failures]},
            "fewshot": asdict(fewshot_result) | {"failures": [asdict(f) for f in fewshot_result.failures]}
        },
        "A8_playbook": playbook
    }
    
    with open(args.out, 'w') as f:
        json.dump(artifact, f, indent=2)
    
    print(f"\n✓ Artifact saved to {args.out}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
