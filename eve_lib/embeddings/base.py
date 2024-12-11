


from abc import ABC, abstractmethod
from typing import List


class Embeddings(ABC):

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """向量化文档"""

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """向量化文本"""