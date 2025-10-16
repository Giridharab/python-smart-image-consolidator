# llm_explainer.py
import os
import openai

# Make sure your OpenAI API key is set in the environment
# export OPENAI_API_KEY="your_api_key"
openai.api_key = os.getenv("OPENAI_API_KEY")


def explain_suggestion(current_base: str, suggested_base: str) -> str:
    """
    Calls OpenAI GPT to explain why the suggested base image is recommended.

    Parameters:
        current_base (str): The current Docker base image.
        suggested_base (str): The suggested canonical base image.

    Returns:
        str: Explanation text from GPT.
    """
    try:
        prompt = (
            f"I have a Docker image based on '{current_base}', "
            f"and I am considering switching it to '{suggested_base}'. "
            "Explain why this change might be beneficial, "
            "including advantages, potential risks, and any compatibility issues."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        explanation = response['choices'][0]['message']['content'].strip()
        return explanation

    except Exception as e:
        # Fallback in case of API errors
        return f"Could not generate explanation due to error: {e}"