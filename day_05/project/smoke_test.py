"""
Minimal smoke test for the Day 5 brochure pipeline.

Prerequisites:
    .env configured for Azure OpenAI access (see day_05/project/main.py)

Usage:
  python day_05/project/smoke_test.py
    python day_05/project/smoke_test.py --url https://www.python.org --output day_05/project/smoke_output.json
  python day_05/project/smoke_test.py --company "OpenAI" --output day_05/project/smoke_output.json
    python day_05/project/smoke_test.py --company "OpenAI" --llm-timeout 30 --llm-retries 1
"""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from day_05.project.main import (
    collect_research,
    generate_brochure_json,
    save_output,
    validate_brochure,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke test for brochure pipeline")
    parser.add_argument("--url", type=str, default=None, help="Optional company URL")
    parser.add_argument("--company", type=str, default="OpenAI", help="Company name")
    parser.add_argument(
        "--llm-timeout",
        type=float,
        default=30.0,
        help="LLM request timeout in seconds",
    )
    parser.add_argument(
        "--llm-retries",
        type=int,
        default=1,
        help="Max retries for LLM call failures",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="day_05/project/smoke_output.json",
        help="Output path for validated brochure",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.llm_timeout <= 0:
        raise SystemExit("--llm-timeout must be greater than 0")
    if args.llm_retries < 0:
        raise SystemExit("--llm-retries must be 0 or greater")

    research = collect_research(args.url, args.company)
    brochure_dict = generate_brochure_json(
        research,
        llm_timeout=args.llm_timeout,
        llm_retries=args.llm_retries,
    )
    validated = validate_brochure(brochure_dict)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_output(validated, str(output_path))

    print("Smoke test passed")
    print(f"Output saved to: {output_path}")
    print(f"Company: {validated.company_name}")
    print(f"what_company_does bullets: {len(validated.what_company_does)}")
    print(f"achievements bullets: {len(validated.achievements)}")


if __name__ == "__main__":
    main()
