from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, Optional

from eve_lib.embeddings.base import Embeddings
from eve_lib.schema import Document


class VectorStore(ABC):

    @abstractmethod
    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        """查询相似的文档"""

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        embedding: Embeddings,
        **kwargs: Any
    ) -> VectorStore:
        texts = [d.page_content for d in documents]
        metadatas = [d.metadata for d in documents]
        return cls.from_texts(texts=texts, embedding=embedding, metadatas=metadatas, **kwargs)


    @classmethod
    @abstractmethod
    def from_texts(
        cls, 
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        **kwargs
    ) -> VectorStore:
        """根据texts和embedding初始化vectorStore"""