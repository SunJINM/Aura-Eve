from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pydantic import BaseModel


class BaseLLM(BaseModel, ABC):


    @abstractmethod
    def _generate(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """文本生成抽象方法,由继承类实现"""

    def generate(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            output = self._generate(prompt, stop=stop)
        except (KeyboardInterrupt, Exception) as e:
            raise e
        return output

    def __call__(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return self.generate(prompt, stop=stop)