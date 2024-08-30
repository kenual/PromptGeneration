import os
import chainlit as cl
from chainlit.cli import run_chainlit
from prompt_poet import Prompt
from g4f_util import DEFAULT_MODEL, get_async_completion
from template_util import get_template_path

CWD = os.path.dirname(__file__)
MESSAGE_HISTORY_KEY = 'message_history'

@cl.on_chat_start
def start_chat():
    prompt = Prompt(template_data={}, template_path=get_template_path(CWD, 'system_prompt.yml'))    
    cl.user_session.set(
        MESSAGE_HISTORY_KEY, prompt.messages
    )

@cl.on_message
async def main(message: cl.Message):
    messages = cl.user_session.get(MESSAGE_HISTORY_KEY)

    llm_response = cl.Message(content='')
    await llm_response.send()

    messages.append({'role': 'user', 'content': message.content})
    response = await get_async_completion(messages, DEFAULT_MODEL, llm_response)
    await llm_response.update()
    
    messages.append({'role': 'assistant', 'content': response})

@cl.on_chat_end
def on_chat_end():
    cl.user_session.set(
        MESSAGE_HISTORY_KEY, []
    )

def main():
    run_chainlit(__file__)

if __name__ == '__main__':
    main()