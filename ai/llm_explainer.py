from openai import OpenAI
import os

def explain_suggestion(original_base, suggested_base):
    """
    Generates an AI-based explanation for Docker base image changes using Cisco's internal LLM proxy.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = "https://llm-proxy.us-east-2.int.infra.intelligence.webex.com/openai/v1"

    if not api_key:
        return "Error: OPENAI_API_KEY not found in environment."

    client = OpenAI(api_key=api_key, base_url=base_url)

    prompt = f"""
    Analyze Dockerfile base image change:

    - Original Base: {original_base}
    - Suggested Base: {suggested_base}

    Provide:
    1. Why this change was recommended.
    2. Potential risks (compatibility/security).
    3. Rollback plan if issues occur.
    4. Expected improvements in performance, cost, or security.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are an expert DevOps assistant specialized in Docker optimization."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Could not generate explanation due to error: {e}"
