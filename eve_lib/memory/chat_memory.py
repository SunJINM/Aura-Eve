
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from eve_lib.memory.utils import get_prompt_input_key
from eve_lib.schema import AIMessage, BaseMemory, BaseMessage, HumanMessage


class ChatMessageHistory(BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_user_message(self, message: str) -> None:
        self.messages.append(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        self.messages.append(AIMessage(content=message))
    
    def clear(self) -> None:
        self.messages = []


class BaseChatMemory(BaseMemory, BaseModel):

    chat_memory: ChatMessageHistory = Field(default_factory=ChatMessageHistory)
    input_key: Optional[str] = None
    output_key: Optional[str] = None

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError("只能有一个输出key")
            output_key = list(outputs.keys())[0]
        else:
            output_key = self.output_key
        self.chat_memory.add_user_message(inputs[prompt_input_key])
        self.chat_memory.add_ai_message(outputs[output_key])

    
    def clear(self) -> None:
        self.chat_memory.clear()