import json
from typing import List, Optional

from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError
)
from openai import OpenAI
from openai.types.chat import ChatCompletion

from bwt.logger import get_logger


class Prompter:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.logger = get_logger("Prompter")

    def __call__(self, content: str, messages: List[str]) -> Optional[List[str]]:
        try:
            response = self._get_response(content, messages)
        except (APIConnectionError, APITimeoutError, InternalServerError) as exception:
            self.logger.error(f"OpenAI error: {exception}")
            return None

        message = self._retrieve_message(response)

        try:
            return json.loads(message)
        except json.JSONDecodeError:
            self.logger.error(f"JSON parser error: {message}")

    def _get_response(self, content: str, messages: List[str]) -> ChatCompletion:
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

    @staticmethod
    def _retrieve_message(response: ChatCompletion) -> str:
        message = response.choices[0].message.content
        message = message.replace("```json", "")
        message = message.replace("```", "")
        return message
