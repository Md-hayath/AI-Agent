"""LLM helper for setup suggestions and failure explanations."""

import os

from openai import OpenAI


class LLMAgent:
    """Thin wrapper around OpenAI chat completions."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.client = OpenAI(api_key=api_key) if api_key else None

    def is_configured(self) -> bool:
        return self.client is not None

    def suggest_fix(self, task_name: str, task_type: str, error_output: str) -> str:
        if not self.client:
            return "LLM is not configured. Add OPENAI_API_KEY to .env."

        prompt = (
            "You are helping a Windows setup automation agent.\n"
            f"Task name: {task_name}\n"
            f"Task type: {task_type}\n"
            f"Failure output:\n{error_output}\n\n"
            "Give a short, practical fix in 3 bullet points max."
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You give concise Windows troubleshooting steps.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
