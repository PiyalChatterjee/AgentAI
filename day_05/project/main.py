"""
Day 5 Project: AI Brochure Generator

End-to-end pipeline:
1) Collect research from URL/company input
2) Generate brochure JSON via Azure OpenAI
3) Validate output against BrochureOutput schema
4) Save validated JSON to disk

Required environment variables:
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_DEPLOYMENT_NAME
- AZURE_OPENAI_API_VERSION (optional, default set in code)

Example usage:
    python day_05/project/main.py --company "OpenAI" --output day_05/project/brochure.json
    python day_05/project/main.py --url https://www.python.org --output day_05/project/brochure.json
"""

from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List
import argparse
import re
import json
import os
import sys

import requests
from openai import AzureOpenAI
from openai import APIError, APIStatusError
from dotenv import load_dotenv

load_dotenv()


# =========================
# 1) OUTPUT CONTRACT (Pydantic models)
# =========================
class BrochureOutput(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=120)
    what_company_does: List[str] = Field(..., min_length=3, max_length=8)
    journey_and_impact: List[str] = Field(..., min_length=2, max_length=6)
    brief_history: List[str] = Field(..., min_length=2, max_length=6)
    achievements: List[str] = Field(..., min_length=2, max_length=8)
    confidence_note: str = Field(..., min_length=10, max_length=220)

    @field_validator("what_company_does", "journey_and_impact", "brief_history", "achievements")
    @classmethod
    def bullet_quality(cls, value: List[str]) -> List[str]:
        cleaned = [v.strip() for v in value if v and v.strip()]
        if len(cleaned) != len(value):
            raise ValueError("Empty bullet points are not allowed")
        if any(len(v) < 8 for v in cleaned):
            raise ValueError("Each bullet should be meaningful (min 8 chars)")
        return cleaned

# =========================
# 2) INPUT PARSING (CLI args)
# =========================
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a structured company brochure JSON")
    parser.add_argument("--url", type=str, help="URL of the company")
    parser.add_argument("--company", type=str, help="Name of the company")
    parser.add_argument("--output", type=str, default="brochure.json", help="Output file path for the brochure JSON")
    parser.add_argument(
        "--llm-timeout",
        type=float,
        default=None,
        help="LLM request timeout in seconds (fallback: AZURE_OPENAI_TIMEOUT, default 30)",
    )
    parser.add_argument(
        "--llm-retries",
        type=int,
        default=None,
        help="Max retries for LLM call failures (fallback: AZURE_OPENAI_RETRIES, default 1)",
    )
    return parser.parse_args()


# =========================
# 3) RESEARCH (URL/company collection)
# =========================
def _extract_html_research(html: str) -> dict:
    def _clean_text(value: str) -> str:
        return re.sub(r"\s+", " ", value).strip()

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    title = _clean_text(title_match.group(1)) if title_match else ""

    meta_description = ""
    meta_patterns = [
        r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\'](.*?)["\']',
        r'<meta[^>]*name=["\']twitter:description["\'][^>]*content=["\'](.*?)["\']',
    ]
    for pattern in meta_patterns:
        meta_match = re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL)
        if meta_match:
            meta_description = _clean_text(meta_match.group(1))
            if meta_description:
                break

    if not meta_description:
        json_ld_matches = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        for block in json_ld_matches[:5]:
            desc_match = re.search(r'"description"\s*:\s*"(.*?)"', block, flags=re.DOTALL)
            if desc_match:
                meta_description = _clean_text(desc_match.group(1).replace("\\\"", '"'))
                if meta_description:
                    break

    paragraph_matches = re.findall(r"<p[^>]*>(.*?)</p>", html, flags=re.IGNORECASE | re.DOTALL)
    snippets = []
    for raw in paragraph_matches:
        text = re.sub(r"<[^>]+>", " ", raw)
        text = _clean_text(text)
        if len(text) >= 60:
            snippets.append(text)
        if len(snippets) >= 5:
            break

    if len(snippets) < 3:
        cleaned_html = re.sub(
            r"<(script|style|noscript|svg|iframe)[^>]*>.*?</\1>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        body_text = re.sub(r"<[^>]+>", " ", cleaned_html)
        body_text = _clean_text(body_text)
        sentence_candidates = re.split(r"(?<=[.!?])\s+", body_text)
        for sentence in sentence_candidates:
            candidate = _clean_text(sentence)
            if 80 <= len(candidate) <= 300 and candidate not in snippets:
                snippets.append(candidate)
            if len(snippets) >= 5:
                break

    return {
        "title": title,
        "meta_description": meta_description,
        "snippets": snippets,
    }


def collect_research(url, company):
    if url:
        try:
            headers = {"User-Agent": "Mozilla/5.0 AgentAI-Brochure-Research/1.0"}
            response = requests.get(url, timeout=20, headers=headers)
            response.raise_for_status()
            extracted = _extract_html_research(response.text)

            inferred_name = company
            if not inferred_name and extracted["title"]:
                inferred_name = extracted["title"].split("|")[0].split("-")[0].strip()

            return {
                "source": "url",
                "company_name": inferred_name or "Unknown Company",
                "source_url": url,
                "title": extracted["title"],
                "meta_description": extracted["meta_description"],
                "snippets": extracted["snippets"] or [f"Limited public content extracted from {url}"],
            }
        except requests.RequestException as exc:
            return {
                "source": "url_fallback",
                "company_name": company or "Unknown Company",
                "source_url": url,
                "title": company or "",
                "meta_description": "",
                "snippets": [f"URL fetch failed: {str(exc)}"],
            }

    if company:
        return {
            "source": "company",
            "company_name": company,
            "source_url": None,
            "title": company,
            "meta_description": "",
            "snippets": [f"Public profile summary for {company} is required."],
        }

    raise ValueError("No valid input provided")


# =========================
# 4) GENERATION (LLM brochure JSON)
# =========================
def generate_brochure_json(research, llm_timeout: float = 30.0, llm_retries: int = 1):
    """
    Call Azure OpenAI to transform research data into structured BrochureOutput JSON.
    
    Input: research dict from collect_research (has company_name, snippets, title, meta_description)
    Output: dict matching BrochureOutput field names and structure
    """
    if llm_timeout <= 0:
        raise ValueError("llm_timeout must be > 0 seconds")
    if llm_retries < 0:
        raise ValueError("llm_retries must be >= 0")

    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not deployment:
        # Backward compatibility for older environment naming.
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not api_key or not endpoint:
        raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT in .env")
    if not deployment:
        raise ValueError("Missing AZURE_OPENAI_DEPLOYMENT_NAME (or legacy AZURE_OPENAI_DEPLOYMENT) in .env")
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        azure_endpoint=endpoint,
    )
    
    system_prompt = (
        "You are an expert business analyst. "
        "Return ONLY a strict JSON object with no markdown fences and no additional commentary."
    )
    user_prompt = f"""
Analyze this company and generate a professional brochure profile as JSON.

Company: {research.get('company_name', 'Unknown')}
Source Title: {research.get('title', '')}
Description: {research.get('meta_description', '')}
Content Snippets:
{chr(10).join(f"- {s[:200]}" for s in research.get('snippets', []))}

Return ONLY a JSON object with these exact fields (no extra text, no markdown):
{{
    "company_name": "string, 2-120 chars",
    "what_company_does": ["3 to 8 bullets, each >= 8 chars"],
    "journey_and_impact": ["2 to 6 bullets, each >= 8 chars"],
    "brief_history": ["2 to 6 bullets, each >= 8 chars"],
    "achievements": ["2 to 8 bullets, each >= 8 chars"],
    "confidence_note": "string, 10-220 chars"
}}

Rules:
1) Provide at least the minimum number of bullets required in each list.
2) Use complete meaningful statements, not fragments.
3) If data is limited, infer cautiously and mention uncertainty in confidence_note.
4) Output must be valid JSON parsable by json.loads.
"""
    
    last_exc = None
    response = None
    for _ in range(max(llm_retries, 0) + 1):
        try:
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1500,
                timeout=llm_timeout,
            )
            break
        except (APIError, APIStatusError) as exc:
            last_exc = exc

    if response is None:
        raise ValueError(f"LLM request failed after retries: {last_exc}")
    
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from Azure OpenAI")
    response_text = content.strip()

    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    try:
        brochure_dict = json.loads(response_text)
    except json.JSONDecodeError:
        repair_prompt = (
            "Convert the following content into valid JSON only. "
            "Keep exactly these keys: company_name, what_company_does, journey_and_impact, "
            "brief_history, achievements, confidence_note.\n\n"
            f"Content to repair:\n{response_text}"
        )
        repair_response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": repair_prompt},
            ],
            temperature=0,
            max_tokens=1200,
            timeout=llm_timeout,
        )
        repaired_content = repair_response.choices[0].message.content
        if not repaired_content:
            raise ValueError("JSON repair attempt returned empty content")
        repaired_text = repaired_content.strip()
        if repaired_text.startswith("```"):
            repaired_text = repaired_text.split("```")[1]
            if repaired_text.startswith("json"):
                repaired_text = repaired_text[4:]
            repaired_text = repaired_text.strip()
        brochure_dict = json.loads(repaired_text)

    # Enforce minimum sizes expected by BrochureOutput before validation.
    min_counts = {
        "what_company_does": 3,
        "journey_and_impact": 2,
        "brief_history": 2,
        "achievements": 2,
    }
    for key, minimum in min_counts.items():
        raw_items = brochure_dict.get(key, [])
        if not isinstance(raw_items, list):
            raw_items = [str(raw_items)] if raw_items else []
        cleaned = [str(item).strip() for item in raw_items if str(item).strip()]
        while len(cleaned) < minimum:
            cleaned.append(
                f"Limited public information was available; this point is an inferred summary for {brochure_dict.get('company_name', 'the company')}."
            )
        brochure_dict[key] = cleaned

    if "company_name" not in brochure_dict or not str(brochure_dict["company_name"]).strip():
        brochure_dict["company_name"] = research.get("company_name", "Unknown Company")

    if "confidence_note" not in brochure_dict or not str(brochure_dict["confidence_note"]).strip():
        brochure_dict["confidence_note"] = "Generated from limited public context; some points may require confirmation."

    return brochure_dict


# =========================
# 5) VALIDATION (Pydantic parse/validate)
# =========================
def validate_brochure(data):
    """
    Parse and validate the LLM-generated brochure JSON dict into BrochureOutput model.
    
    Input: dict with brochure fields (company_name, what_company_does, etc.)
    Output: validated BrochureOutput instance
    Raises: ValidationError if data doesn't match schema
    """
    try:
        brochure = BrochureOutput(**data)
        return brochure
    except Exception as e:
        raise ValueError(f"Brochure validation failed: {e}")


# =========================
# 6) OUTPUT (save/format)
# =========================
def save_output(validated, output_path):
    """
    Serialize validated BrochureOutput model to JSON and save to file.
    
    Input: validated BrochureOutput instance and output file path
    Output: None (writes file)
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(validated.model_dump_json(indent=2))
    except IOError as e:
        raise ValueError(f"Failed to save brochure to {output_path}: {e}")


# =========================
# 7) ERROR HANDLING + ORCHESTRATION
# =========================
def _normalize_inputs(url: str | None, company: str | None) -> tuple[str | None, str | None]:
    normalized_url = url.strip() if url else None
    normalized_company = company.strip() if company else None

    if normalized_url and not normalized_url.startswith(("http://", "https://")):
        normalized_url = f"https://{normalized_url}"

    return normalized_url, normalized_company


def _resolve_llm_controls(args: argparse.Namespace) -> tuple[float, int]:
    env_timeout_raw = os.getenv("AZURE_OPENAI_TIMEOUT")
    env_retries_raw = os.getenv("AZURE_OPENAI_RETRIES")

    try:
        llm_timeout = args.llm_timeout if args.llm_timeout is not None else float(env_timeout_raw) if env_timeout_raw else 30.0
    except ValueError as exc:
        raise ValueError(f"Invalid AZURE_OPENAI_TIMEOUT value: {env_timeout_raw}") from exc

    try:
        llm_retries = args.llm_retries if args.llm_retries is not None else int(env_retries_raw) if env_retries_raw else 1
    except ValueError as exc:
        raise ValueError(f"Invalid AZURE_OPENAI_RETRIES value: {env_retries_raw}") from exc

    if llm_timeout <= 0:
        raise ValueError("llm-timeout must be greater than 0")
    if llm_retries < 0:
        raise ValueError("llm-retries must be 0 or greater")

    return llm_timeout, llm_retries


def main():
    args = parse_args()
    url, company = _normalize_inputs(args.url, args.company)
    llm_timeout, llm_retries = _resolve_llm_controls(args)

    if not url and not company:
        raise SystemExit("Provide at least one input: --url or --company")

    try:
        research = collect_research(url, company)
        brochure_json = generate_brochure_json(research, llm_timeout=llm_timeout, llm_retries=llm_retries)
        validated_brochure = validate_brochure(brochure_json)
        save_output(validated_brochure, args.output)
        print(f"Brochure successfully generated and saved to {args.output}")
    except requests.RequestException as e:
        print(f"Network error while collecting research: {e}")
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        print(f"Model returned invalid JSON: {e}")
        raise SystemExit(1)
    except ValidationError as e:
        print(f"Generated brochure failed schema validation: {e}")
        raise SystemExit(1)
    except APIStatusError as e:
        print(f"Azure OpenAI request failed with status {e.status_code}: {e}")
        raise SystemExit(1)
    except APIError as e:
        print(f"Azure OpenAI API error: {e}")
        raise SystemExit(1)
    except ValueError as e:
        print(f"Input or processing error: {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Execution interrupted by user")
        sys.exit(130)

