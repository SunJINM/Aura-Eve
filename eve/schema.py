from __future__ import annotations

from typing import Any, Dict
from pydantic import BaseModel


class EmotionState(BaseModel):
    state: float
    explanation: str

    @classmethod
    def from_json(cls, emotion: Dict[str, Any]) -> EmotionState:
        return cls(state=emotion["state"], explanation=emotion["explanation"])

class BaseEmotionState(BaseModel):
    joy_sadness: EmotionState
    anger_calmness: EmotionState
    trust_distrust: EmotionState
    anticipation_disappointment: EmotionState
    surprise_normalcy: EmotionState
    fear_security: EmotionState

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_json(cls, emotions: Dict[str, Any]) -> BaseEmotionState:
        return cls(**{k: EmotionState.from_json(emotions[k]) for k in emotions.keys()})
    
    @classmethod
    def from_dict(cls, data: Dict[str, EmotionState]) -> BaseEmotionState:
        return cls(**data)
            

class HistoryEmotion(BaseModel):
    timestamp: Any
    emotional_state: BaseEmotionState