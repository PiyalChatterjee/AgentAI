"""
Day 1: Chatbot with 3 System Prompts
Compares outputs from friendly teacher, technical expert, and product manager roles
Run: python day1_chatbot.py
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# ======== SETUP ========
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") # Ensure this is the base URL
)


# Fixed user question for all comparisons
USER_QUESTION = "Explain OpenAI to me as a newly admitted student"

# Three system prompts
PROMPTS = {
    "friendly_teacher": """you are a teacher
explain to me openAI as a newly admitted student
use exactly 8 bullets, each bullet max 14 words
"Bullet 1: one-line definition"
"Bullets 2-4: practical uses"
"Bullets 5-6: limitations/safety"
"Bullet 7: example"
"Bullet 8: recap"
no headings, no subsections
use polite and simple terms to explain
give the output in bullet terms""",

    "technical_expert": """you are a senior AI research engineer
explain openAI with technical precision and depth
use exactly 8 bullets, each bullet max 14 words
"Bullet 1: technical definition"
"Bullets 2-4: architectural components or key innovations"
"Bullets 5-6: limitations or research challenges"
"Bullet 7: cite one foundational paper or concept"
"Bullet 8: research direction summary"
no explanatory text before bullets
assume audience has CS fundamentals
give output as numbered bullets only""",

    "product_manager": """you are a product manager at a tech company
explain openAI from market and user value perspective
use exactly 8 bullets, each bullet max 14 words
"Bullet 1: market positioning in one sentence"
"Bullets 2-4: customer pain points this solves"
"Bullets 5-6: competitive advantages or moat"
"Bullet 7: pricing or business model insight"
"Bullet 8: future product direction prediction"
no headers, no fluff
focus on business impact and outcomes
output as bulleted list only"""
}

# ======== FUNCTIONS ========
def call_api(system_prompt, user_question, model=None):
    """
    Make a single API call with given system prompt.
    Returns: response text, token count, and finish reason
    
    NOTE: 'model' parameter is the DEPLOYMENT NAME in Azure, not the model name
    """
    try:
        deployment_name = model or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        if not deployment_name:
            return {
                "error": "AZURE_OPENAI_DEPLOYMENT_NAME is not set. Add it to .env.",
                "text": None,
                "tokens_used": 0,
            }

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
            max_tokens=200,
            top_p=0.9,
        )
        
        return {
            "text": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
            "finish_reason": response.choices[0].finish_reason,
            "model": response.model
        }
    except Exception as e:
        return {
            "error": str(e),
            "text": None,
            "tokens_used": 0
        }

def compare_prompts():
    """
    Run all 3 system prompts and compare outputs.
    Save results to JSON for later review.
    """
    print("=" * 80)
    print("DAY 1 CHATBOT: 3-PROMPT COMPARISON")
    print("=" * 80)
    print(f"\nUser Question: {USER_QUESTION}\n")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "user_question": USER_QUESTION,
        "responses": {}
    }
    
    # Run each prompt
    for role_name, system_prompt in PROMPTS.items():
        print(f"\n{'=' * 80}")
        print(f"ROLE: {role_name.upper()}")
        print(f"{'=' * 80}")
        
        # API call
        response = call_api(system_prompt, USER_QUESTION)
        
        if "error" in response:
            print(f"❌ ERROR: {response['error']}")
            results["responses"][role_name] = response
        else:
            # Display
            print(response["text"])
            print(f"\n📊 Metrics:")
            print(f"   Tokens used: {response['tokens_used']}")
            print(f"   Finish reason: {response['finish_reason']}")
            print(f"   Model: {response['model']}")
            
            # Store
            results["responses"][role_name] = response
    
    # Save results
    output_file = "day1_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    return results

# ======== MANUAL TESTING ========
def test_single_prompt(role_name):
    """
    Test a single prompt interactively.
    Use for debugging or manual testing.
    """
    if role_name not in PROMPTS:
        print(f"❌ Unknown role: {role_name}")
        print(f"   Available: {list(PROMPTS.keys())}")
        return
    
    print(f"\n🔧 Testing: {role_name}")
    response = call_api(PROMPTS[role_name], USER_QUESTION)
    print(response["text"])

# ======== MAIN ========
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test single prompt: python day1_chatbot.py friendly_teacher
        test_single_prompt(sys.argv[1])
    else:
        # Run full comparison
        compare_prompts()
