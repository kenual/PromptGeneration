import os
import chainlit as cl
from prompt_poet import Prompt
from g4f_util import get_completion

CWD = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(
    CWD, "../templates", "prompt_generation.yml.j2"))

@cl.on_message
async def main(message: cl.Message):
    template_data = {
        'user_query': message.content
    }
    prompt = Prompt(template_data=template_data, template_path=template_path)
    response = get_completion(messages=prompt.messages)
    markdown = response.lstrip('```markdown').rstrip('```')

    messages = [{'role': 'user', 'content': markdown}]
    response = get_completion(
        messages=messages)

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()