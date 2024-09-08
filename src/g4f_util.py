from typing import AsyncIterator
from g4f.client import ChatCompletionChunk, Client
from g4f.models import gpt_4o
from g4f.typing import Messages
from chainlit import Message

DEFAULT_MODEL = gpt_4o.name

def get_completion(
    messages: Messages,
    model: str = DEFAULT_MODEL
) -> str:
    client = Client()
    return process_chat_completion_response(
        client=client, model=model, messages=messages
    )

async def get_async_completion(
        messages: Messages,
        model: str,
        ui_message: Message
) -> AsyncIterator[ChatCompletionChunk]:
    client = Client()
    return await collect_async_chat_completion_response(
        client=client, model=model, messages=messages,
        ui_message=ui_message
    )

async def collect_async_chat_completion_response(
    client: Client,
    model: str,
    messages: Messages,
    ui_message: Message
) -> str:
    chat_completion = client.chat.completions.create(
            model=model, messages=messages, stream=True
    )

    msg = ''
    for chunk in chat_completion:
        token = chunk.choices[0].delta.content
        if token:
            await ui_message.stream_token(token)
            msg += token
    return msg

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
