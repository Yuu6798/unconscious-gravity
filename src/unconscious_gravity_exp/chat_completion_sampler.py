"""Simple sampler for OpenAI chat completions."""

from typing import List
import openai


class ChatCompletionSampler:
    """Utility to sample multiple chat completions using the OpenAI API."""

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        """Initialize with target model name."""
        self.model = model

    def sample(self, prompt: str, n: int = 1) -> List[str]:
        """Return ``n`` completions for ``prompt``."""
        resp = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            n=n,
        )
        return [choice.message.content for choice in resp.choices]

