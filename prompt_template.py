from typing import Optional, List
import g4f
from langchain.chains import LLMChain
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate

class G4FLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        out = g4f.Completion.create(
            model  = 'text-davinci-003',
            prompt=prompt,
            provider=g4f.Provider.Bing
        )
        if stop:
            stop_indexes = min(out.find(s) for s in stop if s in out)
            min_stop = min(stop_indexes, default=-1)
            if min_stop > -1:
                out = out[:min_stop]
        return out
    
llm = G4FLLM()


prompt = PromptTemplate(
    input_variables=["product"],
    template=\
"\
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
)

chain = LLMChain(llm=llm, prompt=prompt)

print(chain.run("how to use ChatGPT?"))