
from typing import Any, Dict, List, Mapping, Optional, Tuple
from pydantic import BaseModel, ConfigDict, model_validator
from lib.chat_models.base import BaseChatModel
from lib.schema import AIMessage, BaseMessage, ChatGeneration, ChatMessage, ChatResult, HumanMessage, SystemMessage
from lib.utils import get_from_dict_or_env


def _convert_dict_to_message(_dict: dict) -> BaseMessage:
    role = _dict.role
    if role == "user":
        return HumanMessage(content=_dict.content)
    elif role == "assistant":
        return AIMessage(content=_dict.content)
    elif role == "system":
        return SystemMessage(content=_dict.content)
    else:
        return ChatMessage(content=_dict.content, role=role)


def _convert_message_to_dict(message: BaseMessage) -> dict:
    if isinstance(message, ChatMessage):
        message_dict = {"role": message.role, "content": message.content}
    elif isinstance(message, HumanMessage):
        message_dict = {"role": "user", "content": message.content}
    elif isinstance(message, AIMessage):
        message_dict = {"role": "assistant", "content": message.content}
    elif isinstance(message, SystemMessage):
        message_dict = {"role": "system", "content": message.content}
    else:
        raise ValueError(f"Got unknown type {message}")

    return message_dict

class ChatZhiPuAI(BaseChatModel, BaseModel):

    client: Any
    model_name: str = "glm-4"
    temperature: float = 0.7
    zhipuai_api_key: Optional[str] = None

    model_config = ConfigDict(
        extra='forbid',
        protected_namespaces=()
    )

    @model_validator(mode='before')
    def validate_environment(cls, values: Dict) -> Dict:
        
        zhipuai_api_key = get_from_dict_or_env(
            values, "zhipuai_api_key", "ZHIPUAI_API_KEY"
        )
        try:
            from zhipuai import ZhipuAI

            values['client'] = ZhipuAI(api_key=zhipuai_api_key)

        except ImportError:
            raise ValueError(
                "Could not import zhipuai package"
            )
        return values
    
    @property
    def _default_params(self) -> Mapping[str, Any]:
        return {
            "temperature": self.temperature
        }
    
    def _generate(self, messages: List[BaseMessage], stop: List[str] | None = None) -> ChatResult:
        message_dicts, params = self._create_message_dict(messages, stop)

        response = self.client.chat.completions.create(
            messages=message_dicts,
            **params
        )
        return self._create_chat_result(response=response)

    def _create_message_dict(
        self, messages: List[BaseMessage], stop: Optional[List[str]] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        params: Dict[str, Any] = {**{"model": self.model_name}, **self._default_params}
        if stop is not None:
            params["stop"] = stop
        message_dicts = [_convert_message_to_dict(message) for message in messages]
        return message_dicts, params
    
    def _create_chat_result(self, response: Mapping[str, Any]) -> ChatResult:
        generations = []
        for res in response.choices:
            message = _convert_dict_to_message(res.message)
            gen = ChatGeneration(message=message)
            generations.append(gen)
        return ChatResult(generations=generations)