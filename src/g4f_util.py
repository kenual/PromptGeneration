from g4f.client import Client
from g4f.models import gpt_4o
from g4f.typing import Messages


def get_completion(messages: Messages, model: str = gpt_4o) -> str:
    client = Client()
    chat_completion = client.chat.completions.create(
        model=model, messages=messages)
    response = chat_completion.choices[0].message.content or ""
    return response
