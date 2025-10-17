import os
from openai import OpenAI

# Use proxy endpoint instead of public OpenAI URL
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # Your org-provided key
    base_url="https://llm-proxy.us-east-2.int.infra.intelligence.webex.com/openai/v1"
)

def explain_suggestion(original_base, suggested_base):
    """
    Generate an AI-based explanation for why the Dockerfile base image 
    should change, potential risks, rollback info, and its impact.
    """
    try:
        prompt = f"""
You are an expert DevOps engineer. A Dockerfile uses base image '{original_base}', 
and the system suggests replacing it with '{suggested_base}'.

Provide a concise explanation covering:
1. Why this change is recommended.
2. Potential compatibility or security risks.
3. Rollback considerations if issues arise.
4. What functional improvements or optimizations this change brings.

Format:
**Why:** ...
**Risks:** ...
**Rollback:** ...
**Impact:** ...
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Could not generate explanation due to error: {e}"
