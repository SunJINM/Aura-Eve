
from abc import ABC
from typing import List, Optional
from pydantic import BaseModel
from lib.schema import BaseLanguageModel, BaseMessage, ChatResult, HumanMessage, LLMResult, PromptValue


class BaseChatModel(BaseLanguageModel, BaseModel, ABC):

    def generate(
        self, messages: List[List[BaseMessage]], stop: Optional[List[str]] = None
    ) -> LLMResult:
        results = []
        for m in messages:
            results.append(self._generate(m, stop=stop))
        return LLMResult(generations=[res.generations for res in results])


    def _generate(
        self, messages: List[BaseMessage], stop: Optional[List[str]] = None
    ) -> ChatResult:
        """"""

    def generate_prompt(
        self, prompts: List[PromptValue], stop: Optional[List[str]] = None
    ) -> LLMResult:
        messages = [p.to_messages() for p in prompts]
        return self.generate(messages, stop=stop)
    
    def __call__(self, messages: List[BaseMessage], stop: Optional[List[str]] = None) -> BaseMessage:
        return self._generate(messages, stop=stop).generations[0].message
    
    def call_as_llm(self, message: str, stop: Optional[List[str]] = None) -> str:
        result = self([HumanMessage(content=message)], stop=stop)
        return result.content