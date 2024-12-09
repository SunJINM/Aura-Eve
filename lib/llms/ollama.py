from __future__ import annotations

from typing import Any, Dict, Generator, List, Mapping, Optional
from pydantic import BaseModel, ConfigDict, model_validator
from lib.llms.base import BaseLLM
from lib.schema import Generation, LLMResult


class Ollama(BaseLLM, BaseModel):

    client: Any = None
    model_name: str = "qwen2:7b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7
    top_p: float = 0.9
    n: int = 1

    model_config = ConfigDict(
        extra='allow',
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )

    
    @model_validator(mode='after')
    def validate_environment(cls, values: Ollama) -> Ollama:
        try:
            import ollama
            values.client = ollama.Client(host=values.base_url)

        except ImportError:
            raise ValueError(
                "无法导入ollama包"
            )
        return values
    
    @property
    def _default_params(self) -> Mapping[str, Any]:
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "num_batch": self.n
        }
    
    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        params = self._default_params
        if stop is not None:
            params["stop"] = stop
        choices = []
        for _prompt in prompts:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": _prompt}],
                options=self._default_params
            )
            choices.append(response)
        return self._create_llm_result(choices, prompts)
    
    def _create_llm_result(
        self, 
        choices: Any, 
        prompts: List[str]
    ) -> LLMResult:
        generations = []
        for i, _ in enumerate(prompts):
            choice = choices[i]
            generations.append(
                [
                    Generation(
                        text=choice.message.content,
                        generation_info=dict(
                            finish_reason=choice.done_reason
                        )
                    )
                ]
            )
        llm_output = {"model_name": self.model_name}
        return LLMResult(generations=generations, llm_output=llm_output)
    
    def stream(self, prompt: str, stop: Optional[List[str]] = None) -> Generator:
        generator = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                options=self._default_params
            )
        return generator