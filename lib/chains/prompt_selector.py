

from abc import ABC, abstractmethod
from typing import Callable, List, Tuple
from pydantic import BaseModel, Field

from lib.chat_models.base import BaseChatModel
from lib.llms.base import BaseLLM
from lib.prompts.base import BasePromptTemplate
from lib.schema import BaseLanguageModel


class BasePromptSelector(BaseModel, ABC):

    @abstractmethod
    def get_prompt(self, llm: BaseLanguageModel) -> BasePromptTemplate:
        """根据llm获取prompt"""
    

class ConditionalPromptSelector(BasePromptSelector, BaseModel):

    default_prompt: BasePromptTemplate
    conditionals: List[
        Tuple[Callable[[BaseLanguageModel], bool], BasePromptTemplate]
    ] = Field(default_factory=list)

    def get_prompt(self, llm: BaseLanguageModel) -> BasePromptTemplate:
        for condition, prompt in self.conditionals:
            if condition(llm):
                return prompt
        return self.default_prompt

def is_llm(llm: BaseLanguageModel) -> bool:
    return isinstance(llm, BaseLLM)

def is_chat_model(llm: BaseLanguageModel) -> bool:
    return isinstance(llm, BaseChatModel)
