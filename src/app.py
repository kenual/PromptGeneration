import os
import chainlit as cl
from prompt_poet import Prompt
from g4f_util import get_completion
from template_util import get_template_path

CWD = os.path.dirname(__file__)
MESSAGE_HISTORY_KEY = 'message_history'

async_get_completion = cl.make_async(get_completion)

@cl.on_chat_start
def start_chat():
    prompt = Prompt(template_data={}, template_path=get_template_path(CWD, 'system_prompt.yml'))    
    cl.user_session.set(
        MESSAGE_HISTORY_KEY, prompt.messages
    )

@cl.on_message
async def main(message: cl.Message):
    messages = cl.user_session.get(MESSAGE_HISTORY_KEY)

    msg = cl.Message(content='')
    await msg.send()

    messages.append({'role': 'user', 'content': message.content})

    stream = await async_get_completion(messages=messages, stream=True)
    for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)
    
    messages.append({'role': 'assistant', 'content': msg.content})
    print(messages)
    await msg.update()

@cl.on_chat_end
def on_chat_end():
    cl.user_session.set(
        MESSAGE_HISTORY_KEY, []
    )