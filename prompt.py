import re
import g4f

def role_chat(role: str, message: str) -> list[str]:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": message},
        ],
        provider=g4f.Provider.Bing,
        stream=True,
        temperature=0.2
    )
    return response

def get_gpt_prompt(goal: str) -> str:
    return f"\
I need a best optimized prompt to get ChatGPT to achieve the following user goal\n\
\n\
    {goal}\n\
\n\
Your prompt will be sent to ChatGPT.\n\
The prompt needs to be in bulleted format instructing ChatGPT\n\
    - optimized persona to take on to achieve the above goal\n\
    - the context that customized prompt is based on\n\
    - the desired outcome of the prompt\n\
    - the tone and style of the answer\n\
    - provide a number of options when answering\n\
    - best response output style to explain to the user\n\
Start the prompt with ```\n\
End the prompt with <<END>><<END>>\n\
"

# enter goal
goal = input("Please enter your goal: ")

# confirm user goal
print(f"\nYour goal is:\n{'='*len(goal)}\n{goal}\n{'='*len(goal)}\n")

# streamed completion
PERSONA = "Take the persona of a ChatGPT prompt engineer"
response = role_chat(PERSONA, get_gpt_prompt(goal))

text = ''
for message in response:
    text += message
    print(message, flush=True, end='')
print(end='\n')

results = re.findall(r'```\n(.*?)\n<<END>><<END>>', text, re.DOTALL)
gpt_prompt = results[0]

lines = gpt_prompt.split('\n')
role = lines[0]
prompt = ''.join(lines[1:]) + '\n- Response output is a Markdown page'

response = role_chat(role, prompt)
for message in response:
    print(message, flush=True, end='')
print(end='\n')
