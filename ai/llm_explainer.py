from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment")

client = OpenAI(api_key=api_key)


def explain_suggestion(original_base, suggested_base):
    prompt = f"Explain why '{suggested_base}' is a better Docker base than '{original_base}' in simple terms."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content