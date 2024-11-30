


from typing import Any, Dict, List, Mapping
from pydantic import BaseModel, ConfigDict, model_validator
from eve.llms.base import BaseLLM

from eve.utils import get_from_dict_or_env


class ZhiPuAI(BaseLLM, BaseModel):

    client: Any = None
    model_name: str = "glm-4"
    temperature: float = 0.9

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
            "temperature": self.temperature
        }
    
    def _generate(self, prompt: str, stop: List[str] | None = None) -> str:
        params = self._default_params
        if stop is not None:
            params["stop"] = stop

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            **params
        )
        return response.choices[0].message.content
        