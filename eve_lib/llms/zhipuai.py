
from nt import environ
from typing import Any, Dict, Generator, List, Mapping, Optional, Set
from pydantic import BaseModel, ConfigDict, model_validator
from eve_lib.llms.base import BaseLLM

from eve_lib.schema import Generation, LLMResult
from eve_lib.utils import get_from_dict_or_env

def update_token_usage(
    keys: Set[str], response: Mapping[str, Any], token_usage: Dict[str, Any]
) -> None:
    _keys_to_use = keys.intersection(response.usage)
    for _key in _keys_to_use:
        if _key not in token_usage:
            token_usage[_key] = response.usage._key
        else:
            token_usage[_key] += response.usage._key


class ZhiPuAI(BaseLLM, BaseModel):

    client: Any = None
    model_name: str = "glm-4"
    temperature: float = 0.7
    top_p: float = 0.7
    max_tokens: int = 1024

    model_config = ConfigDict(
        extra='allow',
        protected_namespaces=()
    )

    @model_validator(mode='before')
    def validate_environment(cls, values: Dict) -> Dict:
        
        zhipuai_api_key = get_from_dict_or_env(
            values, "zhipuai_api_key", "ZHIPUAI_API_KEY"
        )
        try:
            from zhipuai import ZhipuAI

            values['client'] = ZhipuAI(api_key=zhipuai_api_key)

        except ImportError:
            raise ValueError(
                "Could not import zhipuai package"
            )
        return values
    
    @property
    def _default_params(self) -> Mapping[str, Any]:
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens
        }
    
    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        params = self._default_params
        if stop is not None:
            params["stop"] = stop
        choices = []
        token_usage: Dict[str, Any] = {}
        _keys = {"completion_tokens", "prompt_tokens", "total_tokens"}
        for _prompt in prompts:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": _prompt}],
                **params
            )
            choices.extend(response.choices)
            update_token_usage(_keys, response, token_usage)
        return self._create_llm_result(choices, prompts, token_usage)
    
    def _create_llm_result(
        self, 
        choices: list, 
        prompts: List[str], 
        token_usage: Dict[str, Any]
    ) -> LLMResult:
        generations = []
        for i, _ in enumerate(prompts):
            choice = choices[i]
            generations.append(
                [
                    Generation(
                        text=choice.message.content,
                        generation_info=dict(
                            finish_reason=choice.finish_reason
                        )
                    )
                ]
            )
        llm_output = {"token_usage": token_usage, "model_name": self.model_name}
        return LLMResult(generations=generations, llm_output=llm_output)
    
    def stream(self, prompt: str, stop: Optional[List[str]] = None) -> Generator:
        params = self.prep_streaming_params(stop)
        generator = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                **params
            )
        return generator
    

    def prep_streaming_params(self, stop: Optional[List[str]] = None) -> Dict[str, Any]:
        params = self._default_params
        if stop is not None:
            if "stop" in params:
                raise ValueError("停止词参数重复")
            params["stop"] = stop
        params["stream"] = True 
        return params
