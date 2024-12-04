from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict, model_validator
from eve.embeddings.base import Embeddings

DEFAULT_MODEL_NAME = "BAAI/bge-base-zh-v1.5"

class HuggingFaceEmbeddings(BaseModel, Embeddings):

    client: Any = None
    model_name: str = DEFAULT_MODEL_NAME
        
    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True,
        protected_namespaces=()
    )

    @model_validator(mode="after")
    def validate_environment(cls, values: HuggingFaceEmbeddings) -> HuggingFaceEmbeddings:
        try:
            import sentence_transformers
            values.client = sentence_transformers.SentenceTransformer(values.model_name)
        except ImportError:
            raise ValueError(
                "无法导入 sentence_transformers 模块"
            )
        return values

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = self.client.encode(texts)
        return embeddings.tolist()
    

    def embed_query(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        embedding = self.client.encode(text)
        return embedding.tolist()