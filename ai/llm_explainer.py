import os
import requests

def explain_suggestion(current_base, suggested_base):
    """
    Generates AI explanation using GitHub Copilot Models API (GPT-4-turbo).
    Requires GITHUB_TOKEN with 'models' access.
    """

    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN not set in environment")

    url = "https://api.github.com/copilot/models/gpt-4-turbo/completions"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/json",
        "X-GitHub-Api-Version": "2023-12-12"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are an expert DevOps assistant."},
            {"role": "user", "content": f"Explain why switching from {current_base} to {suggested_base} is beneficial in terms of security, performance, and cost."}
        ],
        "max_tokens": 300,
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    return result.get("choices", [{}])[0].get("message", {}).get("content", "No explanation available.")