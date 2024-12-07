

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List
from pydantic import BaseModel, ConfigDict

from lib.formatting import formatter
from lib.schema import BaseMessage, HumanMessage, PromptValue


DEFAULT_FORMATTER_MAPPING: Dict[str, Callable] = {
    "f-string": formatter.format
}

def check_valid_template(
    template: str, template_format: str, input_variables: List[str]
) -> None:
    if template_format not in DEFAULT_FORMATTER_MAPPING:
        raise ValueError(
            "不正确的模板格式类型"
        )
    dummy_inputs = {input_variable: "foo" for input_variable in input_variables}
    try:
        DEFAULT_FORMATTER_MAPPING[template_format](template, **dummy_inputs)
    except KeyError as e:
        raise ValueError(
            "提示词模板数据结构错误"
        )

class StringPromptValue(PromptValue):
    text: str

    def to_string(self) -> str:
        return self.text
    
    def to_messages(self) -> List[BaseMessage]:
        return [HumanMessage(content=self.text)]

class BasePromptTemplate(BaseModel, ABC):
    """提示词模板基类"""

    input_variables: List[str]
    """提示词模板需要的参数，为字符串列表"""

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True
    )

    @abstractmethod
    def format_prompt(self, **kwargs: Any) -> PromptValue:
        """格式化提示词，由子类实现"""

    @abstractmethod
    def format(self, **kwargs: Any) -> str:
        """根据输入格式化提示词"""


class StringPromptTemplate(BasePromptTemplate, ABC):

    def format_prompt(self, **kwargs: Any) -> PromptValue:
        return StringPromptValue(text=self.format(**kwargs))