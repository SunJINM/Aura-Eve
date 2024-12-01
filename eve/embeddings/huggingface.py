
from typing import Any, List
from pydantic import BaseModel, ConfigDict
from eve.embeddings.base import Embeddings

DEFAULT_MODEL_NAME = "GanymedeNil/text2vec-large-chinese"

class HuggingFaceEmbeddings(Embeddings, BaseModel):

    client: Any
    model_name: str = DEFAULT_MODEL_NAME

    def __init__(self, **kwargs: Any):
        
        super().__init__(**kwargs)
        try:
            import sentence_transformers
            self.client = sentence_transformers.SentenceTransformer(self.model_name)
        except ImportError:
            raise ValueError(
                "无法导入 sentence_transformers 模块"
            )
        
    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True
    )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = self.client.encode(texts)
        return embeddings.tolist()
    

    def embed_query(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        embedding = self.client.encode(text)
        return embedding.tolist()