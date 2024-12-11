
from typing import Any, Dict, List, Tuple
from pydantic import BaseModel, ConfigDict
from eve_lib.chains.base import Chain
from eve_lib.prompts.base import BasePromptTemplate
from eve_lib.schema import BaseLanguageModel, LLMResult, PromptValue


class LLMChain(Chain, BaseModel):

    prompt: BasePromptTemplate
    llm: BaseLanguageModel
    output_key: str = "text"

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True
    )

    @property
    def input_keys(self) -> List[str]:
        return self.prompt.input_variables
    
    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]
    
    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        """"""
        return self.apply([inputs])[0]
    
    def generate(self, input_list: List[Dict[str, Any]]) -> LLMResult:
        """"""
        prompts, stop = self.prep_prompts(input_list)
        return self.llm.generate_prompt(prompts, stop=stop)

    def prep_prompts(
        self, input_list: List[Dict[str, Any]]
    ) -> Tuple[List[PromptValue], List[str]]:
        stop = None
        if stop in input_list[0]:
            stop = input_list[0]["stop"]
        prompts = []
        for inputs in input_list:
            selected_inputs = {k: inputs[k] for k in self.prompt.input_variables}
            prompt = self.prompt.format_prompt(**selected_inputs)
            if "stop" in inputs and inputs["stop"] != stop:
                raise ValueError(
                    "停止词应该在所有里面，并且等同"
                )
            prompts.append(prompt)
        return prompts, stop
            
    
    def apply(self, input_list: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        response = self.generate(input_list)
        return self.create_outputs(response)
    
    def create_outputs(self, response: LLMResult) -> List[Dict[str, str]]:
        return [
            {self.output_key: generation[0].text}
            for generation in response.generations
        ]
    
    def predict(self, **kwargs: Any) -> str:
        return self(kwargs)[self.output_key]