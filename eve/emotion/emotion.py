from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict

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

    @classmethod
    def from_json(cls, emotions: Dict[str, Any]) -> BaseEmotionState:
        return cls(**{k: EmotionState.from_json(emotions[k]) for k in emotions.keys()})
            



class HistoryEmotion(BaseModel):
    timestamp: Any
    emotional_state: BaseEmotionState

class Emotion(BaseModel):
    current_emotional_state: BaseEmotionState
    historical_emotions: List[HistoryEmotion]
    emotion_decay_rate: float = 0.9

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True 
    )

    

