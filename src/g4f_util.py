from typing import AsyncIterator, Union
from g4f.client import ChatCompletion, ChatCompletionChunk, Client
from g4f.models import gpt_4o
from g4f.typing import Messages


def get_completion(
    messages: Messages,
    model: str = gpt_4o,
    stream: bool = False
) -> Union[str, AsyncIterator[ChatCompletionChunk]]:
    client = Client()
    if stream:
        chat_completion = client.chat.completions.create(
            model=model, messages=messages, stream=stream
        )
        return chat_completion
    else:
        return process_chat_completion_response(
            client=client, model=model, messages=messages
        )


def process_chat_completion_response(
    client: Client,
    model: str,
    messages: Messages
) -> str:
    # Chat Completion Response Format: https://platform.openai.com/docs/guides/chat-completions/response-format
    chat_completion = client.chat.completions.create(
        model=model, messages=messages, stream=False
    )

    if not chat_completion:
        return ''

    finish_reason = chat_completion.choices[0].finish_reason
    if finish_reason == 'stop':
        return chat_completion.choices[0].message.content

    if finish_reason == 'length':
        delta = chat_completion.choices[0].message.content
        return delta + process_chat_completion_response(
            client=client, model=model, messages=messages.append(
                {"role": "assistant", "content": delta}
            )
        )
