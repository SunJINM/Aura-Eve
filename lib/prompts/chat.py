from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Any, List, Union
from pydantic import BaseModel, ConfigDict, Field

from lib.prompts.base import BasePromptTemplate, StringPromptTemplate
from lib.prompts.prompt import PromptTemplate
from lib.schema import (
    BaseMessage,
    ChatMessage,
    HumanMessage,
    AIMessage,
    PromptValue,
    SystemMessage,
    get_buffer_string
)


class BaseMessagePromptTemplate(BaseModel, ABC):
    """"""
    
    @abstractmethod
    def format_messages(self, **kwargs: Any) -> List[BaseMessage]:
        """将输入转为messages"""

    @property
    @abstractmethod
    def input_variables(self) -> List[str]:
        """提示词模板的数据变量"""


class BaseStringMessagePromptTemplate(BaseMessagePromptTemplate, ABC):
    prompt: StringPromptTemplate
    additional_kwargs: dict = Field(default_factory=dict)

    @classmethod
    def from_template(cls, template: str, **kwargs: Any) -> BaseMessagePromptTemplate:
        prompt = PromptTemplate.from_template(template)
        return cls(prompt=prompt, **kwargs)
    
    @abstractmethod
    def format(self, **kwargs: Any) -> BaseMessage:
        """"""

    def format_messages(self, **kwargs: Any) -> List[BaseMessage]:
        return [self.format(**kwargs)]
    
    @property
    def input_variables(self) -> List[str]:
        return self.prompt.input_variables
    

class ChatMessagePromptTemplate(BaseStringMessagePromptTemplate):
    role: str

    def format(self, **kwargs: Any) -> BaseMessage:
        text = self.prompt.format(**kwargs)
        return ChatMessage(content=text, role=self.role, additional_kwargs=self.additional_kwargs)
    

class HumanMessagePromptTemplate(BaseStringMessagePromptTemplate):

    def format(self, **kwargs: Any) -> BaseMessage:
        text = self.prompt.format(**kwargs)
        return HumanMessage(content=text, additional_kwargs=self.additional_kwargs)
    
class AIMessagePromptTemplate(BaseStringMessagePromptTemplate):

    def format(self, **kwargs: Any) -> BaseMessage:
        text = self.prompt.format(**kwargs)
        return AIMessage(content=text, additional_kwargs=self.additional_kwargs)
    

class SystemMessagePromptTemplate(BaseStringMessagePromptTemplate):

    def format(self, **kwargs: Any) -> BaseMessage:
        text = self.prompt.format(**kwargs)
        return SystemMessage(content=text, additional_kwargs=self.additional_kwargs)


class ChatPromptValue(PromptValue):

    messages: List[BaseMessage]

    def to_string(self) -> str:
        return get_buffer_string(self.messages)
    
    def to_messages(self) -> List[BaseMessage]:
        return self.messages



class ChatPromptTemplate(BasePromptTemplate):
    input_variables: List[str]
    messages: List[Union[BaseMessagePromptTemplate, BaseMessage]]


    model_config = ConfigDict(
        extra='forbid'
    )

    @classmethod
    def from_messages(
        cls, messages: List[Union[BaseMessagePromptTemplate, BaseMessage]]
    ) -> ChatPromptTemplate:
        input_vars = set()
        for message in messages:
            if isinstance(message, BaseMessagePromptTemplate):
                input_vars.update(message.input_variables)
        return cls(input_variables=list(input_vars), messages=messages)


    def format_prompt(self, **kwargs: Any) -> PromptValue:
        result = []
        for message_template in self.messages:
            if isinstance(message_template, BaseMessage):
                result.extend([message_template])
            elif isinstance(message_template, BaseMessagePromptTemplate):
                rel_params = {
                    k: v
                    for k, v in kwargs.items()
                    if k in message_template.input_variables
                }
                messages = message_template.format_messages(**rel_params)
                result.extend(messages)
            else:
                raise ValueError("错误输入")
        return ChatPromptValue(messages=result)

    def format(self, **kwargs: Any) -> str:
        return self.format_prompt(**kwargs).to_string()
