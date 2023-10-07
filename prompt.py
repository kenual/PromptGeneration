import re
import g4f

# enter goal
goal = input("Please enter your goal: ")
prompt = f"\
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

# confirm user goal
print(f"\nYour goal is:\n{'='*len(goal)}\n{goal}\n{'='*len(goal)}\n")

# streamed completion
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[
        {"role": "system", "content": "Take the persona of a ChatGPT prompt engineer"},
        {"role": "user", "content": prompt},
    ],
    provider=g4f.Provider.Bing,
    stream=True,
    temperature=0.2
)

text = ''
for message in response:
    text += message
    print(message, flush=True, end='')
print(end='\n')

results = re.findall(r'```\n(.*?)\n<<END>><<END>>', text, re.DOTALL)
print(results[0], end='\n')
