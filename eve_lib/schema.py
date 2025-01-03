from __future__ import annotations


from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


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

class Generation(BaseModel):
    text: str
    """输出内容"""
    generation_info: Optional[Dict[str, Any]] = None
    """其他生成信息"""


class LLMResult(BaseModel):
    generations: List[List[Generation]]

    llm_output: Optional[dict] = None


class ChatGeneration(Generation):
    text: str = ""
    message: BaseMessage

    @model_validator(mode="after")
    def set_text(cls, values: ChatGeneration) -> Dict[str, Any]:
        values.text = values.message.content
        return values
    
class ChatResult(BaseModel):
    generations: List[ChatGeneration]

    llm_output: Optional[dict] = None

class BaseLanguageModel(BaseModel, ABC):

    @abstractmethod
    def generate_prompt(
        self, prompts: List[PromptValue], stop: Optional[List[str]] = None
    ) -> LLMResult:
        """"""


class BaseMemory(BaseModel, ABC):

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True
    )

    @property
    @abstractmethod
    def memory_variables(self) -> List[str]:
        """记忆变量参数"""

    @property
    @abstractmethod
    def load_memory_variables(self) -> Dict[str, Any]:
        """加载记忆"""

    
    @abstractmethod
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """记忆输入和模型输出"""

    @abstractmethod
    def clear(self) -> None:
        """清空记忆"""

class BaseOutputParser(BaseModel, ABC):
    """对llm的输出进行解析处理"""

    @abstractmethod
    def parse(self, text: str) -> Any:
        """处理输出"""