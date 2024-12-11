

from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel

from eve.schema import BaseEmotionState


class BaseAnalyzer(BaseModel, ABC):

    @abstractmethod
    def analyze_query(self, input: str, **kwargs: Any) -> BaseEmotionState:
        """分析问题情感"""