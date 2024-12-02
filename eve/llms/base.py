from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pydantic import BaseModel

from eve.schema import LLMResult


class BaseLLM(BaseModel, ABC):


    @abstractmethod
    def _generate(self, prompt: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        """文本生成抽象方法,由继承类实现"""

    def generate(self, prompt: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        try:
            output = self._generate(prompt, stop=stop)
        except (KeyboardInterrupt, Exception) as e:
            raise e
        return output

    def __call__(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return self.generate(prompt, stop=stop).generations[0][0].text