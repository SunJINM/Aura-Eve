from __future__ import annotations


from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel, Field


def get_buffer_string(
    messages: List[BaseMessage], human_prefix: str = "Human", ai_prefix: str = "AI"
) -> str:
    string_messages = []
    for message in messages:
        if isinstance(message, HumanMessage):
            role = human_prefix
        elif isinstance(message, AIMessage):
            role = ai_prefix
        elif isinstance(message, SystemMessage):
            role = "System"
        elif isinstance(message, ChatMessage):
            role = message.role
        else:
            raise ValueError("不支持该类型消息")
        string_messages.append(f"{role}: {message.content}")
    return "\n".join(string_messages)



class BaseMessage(BaseModel):

    content: str
    additional_kwargs: dict = Field(default_factory=dict)

class PromptValue(BaseModel, ABC):

    @abstractmethod
    def to_string(self) -> str:
        """转为字符串"""

    @abstractmethod
    def to_messages(self) -> List[BaseMessage]:
        """转为消息列表"""

class HumanMessage(BaseMessage):
    """人类的消息"""

class AIMessage(BaseMessage):
    """AI生成的消息"""

class SystemMessage(BaseMessage):
    """系统消息"""

class ChatMessage(BaseMessage):
    role: str
    """消息角色"""

class Document(BaseModel):
    """文档"""
    page_content: str
    """文档内容"""
    metadata: dict = Field(default_factory=dict)
    """文档元数据"""