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
    template="What can we conclude by analyzing data from URL:{url}? Just at least three insights",
)

chain = LLMChain(llm=llm, prompt=prompt)

print(chain.run("https://www.apple.com/newsroom/pdfs/fy2023-q4/FY23_Q4_Consolidated_Financial_Statements.pdf"))