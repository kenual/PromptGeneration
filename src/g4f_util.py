from typing import AsyncIterator, Union
from g4f.client import ChatCompletionChunk, Client
from g4f.models import gpt_4o
from g4f.typing import Messages


def get_completion(
    messages: Messages,
    model: str = gpt_4o,
    stream: bool = False
) -> Union[str, AsyncIterator[ChatCompletionChunk]]:
    client = Client()
    chat_completion = client.chat.completions.create(model=model, messages=messages, stream=stream)
    if stream:
        return chat_completion
    else:
        response = chat_completion.choices[0].message.content or ""
        return response