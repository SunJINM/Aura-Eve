from __future__ import annotations

import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict

from eve.emotions.sentiment_analyzer.base import BaseAnalyzer
from eve.emotions.sentiment_analyzer.llm_analyzer import LLMAnalyzer
from eve.schema import BaseEmotionState, EmotionState, HistoryEmotion
from eve_lib.schema import BaseLanguageModel

class Emotion(BaseModel):
    current_emotional_state: BaseEmotionState
    historical_emotions: List[HistoryEmotion]
    emotion_decay_rate: float = 0.9
    sentiment_analyzer: BaseAnalyzer

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True 
    )

    def update_emotional_state(self, text: str, timestamp: Optional[Any] = None, **kwargs: Any) -> None:
        new_emotional_state = self.sentiment_analyzer.analyze_query(text, **kwargs)

        if self.current_emotional_state is not None:
            self.historical_emotions.append(
                HistoryEmotion(
                    timestamp=timestamp or datetime.now(),
                    emotional_state=self.current_emotional_state
                )
            )

        self.current_emotional_state = self._apply_decay_with_history(
            current_state=self.current_emotional_state,
            historical_states=self.historical_emotions,
            new_state=new_emotional_state,
            decay_rate=self.emotion_decay_rate
        )

    def _apply_decay_with_history(
        self,
        current_state: BaseEmotionState,
        historical_states: List[HistoryEmotion],
        new_state: BaseEmotionState,
        decay_rate: float
    ) -> BaseEmotionState:
        current_emotions = current_state.to_dict()
        new_emotions = new_state.to_dict()

        updated_emotions = {}
        for emotion_type in current_emotions.keys():
            weighted_history = sum(
                entry.emotional_state.to_dict()[emotion_type].state * (decay_rate ** idx)
                for idx, entry in enumerate(reversed(historical_states))
            )

            blended_state = (
                decay_rate * current_emotions[emotion_type].state +
                (1 - decay_rate) * new_emotions[emotion_type].state +
                weighted_history
            )

            updated_emotions[emotion_type] = EmotionState(
                state=max(-1.0, min(1.0, blended_state)),
                explanation=new_emotions[emotion_type].explanation
            )
        return BaseEmotionState.from_dict(updated_emotions)

    def format_emotion_state(current_emotional_state: BaseEmotionState) -> str:
        return f"""
        喜悦-悲伤 (joy_sadness): {current_emotional_state.joy_sadness.state:.2f}
        愤怒-冷静 (anger_calmness): {current_emotional_state.anger_calmness.state:.2f}
        信任-不信任 (trust_distrust): {current_emotional_state.trust_distrust.state:.2f}
        期待-失望 (anticipation_disappointment): {current_emotional_state.anticipation_disappointment.state:.2f}
        惊讶-常态 (surprise_normalcy): {current_emotional_state.surprise_normalcy.state:.2f}
        恐惧-安全 (fear_security): {current_emotional_state.fear_security.state:.2f}
        """
    
    @classmethod
    def from_llm(
        cls, 
        llm: BaseLanguageModel,
        current_emotional_state: Optional[BaseEmotionState] = None,
        historical_emotions: Optional[List[HistoryEmotion]] = None,
        emotion_decay_rate: float = 0.9
    ) -> Emotion:
        current_emotional_state = current_emotional_state or BaseEmotionState(
            joy_sadness=EmotionState(state=0.0, explanation="初始状态"),
            anger_calmness=EmotionState(state=0.0, explanation="初始状态"),
            trust_distrust=EmotionState(state=0.0, explanation="初始状态"),
            anticipation_disappointment=EmotionState(state=0.0, explanation="初始状态"),
            surprise_normalcy=EmotionState(state=0.0, explanation="初始状态"),
            fear_security=EmotionState(state=0.0, explanation="初始状态")
        )
        
        historical_emotions = historical_emotions or []
        emotion_decay_rate = emotion_decay_rate
        sentiment_analyzer = LLMAnalyzer(llm=llm)
        return cls(
            current_emotional_state=current_emotional_state,
            historical_emotions=historical_emotions,
            sentiment_analyzer=sentiment_analyzer
        )