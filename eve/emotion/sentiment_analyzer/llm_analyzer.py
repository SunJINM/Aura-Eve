

import json
from typing import Any
from pydantic import BaseModel
from eve.emotion.emotion import BaseEmotionState
from eve.emotion.sentiment_analyzer.base import BaseAnalyzer
from eve.emotion.sentiment_analyzer.prompt import PROMPT
from lib.prompts.prompt import PromptTemplate
from lib.schema import BaseLanguageModel, BaseMessage, get_buffer_string

class LLMAnalyzer(BaseAnalyzer, BaseModel):
    llm: BaseLanguageModel
    prompt: PromptTemplate = PROMPT


    def analyze_query(self, input: str, **kwargs: Any) -> BaseEmotionState:
        chat_history_str = ""
        if "chat_history" in kwargs:
            chat_history = kwargs["chat_history"]
            if isinstance(chat_history, str):
                chat_history_str = chat_history
            elif isinstance(chat_history, list) and isinstance(chat_history[0], BaseMessage):
                chat_history_str = get_buffer_string(chat_history)
            else:
                raise ValueError("历史对话格式非法")
        prompt = self.prompt.format(input=input, chat_history=chat_history_str)
        output = self.llm(prompt)
        return self.extract_emotion(output)
        
    
    def extract_emotion(self, text: str) -> BaseEmotionState:
        try:
            _, emotion, _ = text.split("```")
            emotion_json = json.loads(emotion.strip())
            print(emotion_json)
            return BaseEmotionState.from_json(emotion_json)
        except Exception:
            raise ValueError(f"无法解析输出: {text}")
        
