import os
from prompt_poet import Prompt
from g4f_util import get_completion

CWD = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(
    CWD, "../templates", "prompt_generation.yml.j2"))

while True:
    user_input = input('Describe a new task you want to complete❓\n🤔\n\n')
    if user_input.lower() in ['', 'exit', 'quit']:
        break
    print()

    template_data = {
        'user_query': user_input
    }
    prompt = Prompt(template_data=template_data, template_path=template_path)
    print(f'📧\n\n{prompt.messages}', end='\n\n')

    response = get_completion(messages=prompt.messages)
    # print(f'🤖\n{response}', end='\n\n')
    markdown = response.lstrip('```markdown').rstrip('```')

    print(f'📃\n{markdown}', end='\n\n')
    messages = [{'role': 'user', 'content': markdown}]
    response = get_completion(
        messages=messages)
    print(f'🤖\n\n{response}', end='\n\n')
    messages.append({'role': 'assistant', 'content': response})

    while True:
        user_input = input('👩💭\n\n')
        if user_input.lower() in ['', 'exit', 'quit']:
            break
        print()

        messages.append({'role': 'user', 'content': user_input})
        response = get_completion(messages=messages)
        print(f'🤖\n\n{response}', end='\n\n')
        messages.append({'role': 'assistant', 'content': response})

    print()