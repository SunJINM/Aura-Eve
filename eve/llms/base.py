from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel


class BaseLLM(BaseModel, ABC):


    @abstractmethod
    def _generate(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """文本生成抽象方法"""

    def generate(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            output = self._generate(prompt, stop=stop)
        except (KeyboardInterrupt, Exception) as e:
            raise e
        return output
