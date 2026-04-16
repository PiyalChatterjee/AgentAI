"""
token_utils.py — count tokens and estimate cost for text and chat messages

Usage examples:
  python token_utils.py -t "Explain tokenization to me"
  python token_utils.py -f sample_messages.json -m gpt-4o-mini -p 0.002

Create a JSON file for messages like:
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Explain tokenization."}
]

"""

import os
import json
import argparse
from dotenv import load_dotenv

import tiktoken

# Load environment variables
load_dotenv()


def get_encoding(model=None):
    try:
        if model:
            return tiktoken.encoding_for_model(model)
    except Exception as e:
        print(f"⚠️  Could not load model-specific encoding: {e}")
        print("   Trying default encoding (requires internet on first run)...")
    
    try:
        return tiktoken.get_encoding("cl100k_base")
    except Exception as e:
        print(f"⚠️  Tiktoken encoding unavailable: {e}")
        print("   Using fallback estimation: 1 token ≈ 4 characters")
        return None


def num_tokens_from_string(text, model=None):
    enc = get_encoding(model)
    if enc:
        return len(enc.encode(text))
    else:
        # Fallback: rough estimation (1 token ≈ 4 chars)
        return max(1, len(text) // 4)


def num_tokens_from_messages(messages, model=None):
    """
    Count tokens for a list of chat messages.
    This follows the common heuristic used for OpenAI chat models.
    Heuristics may change per model; treat counts as best-effort.
    """
    enc = get_encoding(model)

    # Default heuristics (may vary by model)
    if model and "gpt-3.5-turbo-0301" in model:
        tokens_per_message = 4
        tokens_per_name = -1
    else:
        tokens_per_message = 3
        tokens_per_name = 1

    total = 0
    for message in messages:
        total += tokens_per_message
        for k, v in message.items():
            # assume v is str
            if enc:
                total += len(enc.encode(v))
            else:
                # Fallback: rough estimation
                total += max(1, len(v) // 4)
            if k == "name":
                total += tokens_per_name
    total += 3  # assistant priming
    return total


def estimate_cost(total_tokens, price_per_1k):
    return (total_tokens / 1000.0) * price_per_1k


def main():
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
    
    p = argparse.ArgumentParser(description="Count tokens and estimate cost")
    p.add_argument("-t", "--text", help="Text to count tokens for")
    p.add_argument("-f", "--file", help="JSON file containing messages array")
    p.add_argument("-m", "--model", help="Model name or deployment (used to pick encoding)", default=deployment_name)
    p.add_argument("-p", "--price", help="Price per 1000 tokens (e.g. 0.002)", type=float, default=0.002)
    args = p.parse_args()

    if not args.text and not args.file:
        print("Provide --text or --file. See usage examples in file header.")
        return

    if args.text:
        tokens = num_tokens_from_string(args.text, args.model)
        cost = estimate_cost(tokens, args.price)
        print(f"Text tokens: {tokens}")
        print(f"Estimated cost (@{args.price}/1k): ${cost:.6f}")

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as fh:
            messages = json.load(fh)
        tokens = num_tokens_from_messages(messages, args.model)
        cost = estimate_cost(tokens, args.price)
        print(f"Messages tokens: {tokens}")
        print(f"Estimated cost (@{args.price}/1k): ${cost:.6f}")


if __name__ == '__main__':
    main()
