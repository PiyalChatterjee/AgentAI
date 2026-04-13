import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import AzureOpenAI

load_dotenv()

# 1. Define the Schema (Like a TypeScript Interface)
class SalesforceLead(BaseModel):
    name: str
    company: str
    estimated_revenue: int
    technical_stack: list[str]

# 2. Initialize Client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") # Ensure this is the base URL
)

# 3. Request Structured Output
response = client.beta.chat.completions.parse(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    messages=[
        {"role": "system", "content": "You are a sales assistant. Generate a mock lead."},
        {"role": "user", "content": "Create a lead for a Senior Engineer at IBM interested in AI."}
    ],
    response_format=SalesforceLead,
)

lead = response.choices[0].message.parsed
print(f"Lead Name: {lead.name}")
print(f"Revenue: ${lead.estimated_revenue}")
print(f"Stack: {', '.join(lead.technical_stack)}")