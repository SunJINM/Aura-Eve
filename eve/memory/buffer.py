

from typing import Dict, List
from pydantic import BaseModel
from eve.memory.chat_memory import BaseChatMemory
from eve.schema import get_buffer_string


class ConversationBufferMemory(BaseChatMemory, BaseModel):
    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "history"

    @property
    def buffer(self) -> str:
        return get_buffer_string(
            self.chat_memory.messages, 
            human_prefix=self.human_prefix, 
            ai_prefix=self.ai_prefix
        )
    
    @property
    def memory_variables(self) -> List[str]:
        return [self.memory_key]

    @property
    def load_memory_variables(self) -> Dict[str, str]:
        return {self.memory_key: self.buffer}
