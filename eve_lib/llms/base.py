from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pydantic import BaseModel

from eve_lib.schema import BaseLanguageModel, LLMResult, PromptValue


class BaseLLM(BaseLanguageModel, BaseModel, ABC):


    @abstractmethod
    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        """文本生成抽象方法,由继承类实现"""

    def generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        try:
            output = self._generate(prompts, stop=stop)
        except (KeyboardInterrupt, Exception) as e:
            raise e
        return output
    
    def generate_prompt(self, prompts: List[PromptValue], stop: Optional[List[str]] = None) -> LLMResult:
        prompt_strings = [p.to_string() for p in prompts]
        return self.generate(prompt_strings, stop=stop)

    def __call__(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return self.generate([prompt], stop=stop).generations[0][0].text