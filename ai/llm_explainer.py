import openai

def explain_suggestion(original_base, suggested_base):
    prompt = f"Explain why changing Docker base image from {original_base} to {suggested_base} is beneficial."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content