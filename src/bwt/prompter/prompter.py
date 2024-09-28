from typing import List

from openai import OpenAI


class Prompter:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def __call__(self, content: str, messages: List[str]):
        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": content
                },
                *[{
                    "role": "user",
                    "content": message,
                } for message in messages],
            ],
        )
