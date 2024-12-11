from __future__ import annotations

import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

from eve_lib.docstore.base import Docstore
from eve_lib.docstore.in_memory import InMemoryDocstore
from eve_lib.embeddings.base import Embeddings
from eve_lib.schema import Document
from eve_lib.vectorstores.base import VectorStore


def dependable_faiss_import() -> Any:
    try:
        import faiss
    except ImportError:
        raise ValueError(
            "无法找到faiss模块"
        )
    return faiss

class FAISS(VectorStore):

    def __init__(
        self,
        embedding_function: Callable,
        index: Any,
        docstore: Docstore,
        index_to_docstore_id: Dict[int, str]
    ):
        self.embedding_function = embedding_function
        self.index = index
        self.docstore = docstore
        self.index_to_docstore_id = index_to_docstore_id
    
    def similarity_search_with_score_by_vector(
        self, embedding: List[float], k: int = 4
    ) -> List[Tuple[Document, float]]:
        scores, indices = self.index.search(np.array([embedding], dtype=np.float32), k)
        docs = []
        for j, i in enumerate(indices[0]):
            if i == -1:
                continue
            _id = self.index_to_docstore_id[i]
            doc = self.docstore.search(_id)
            if not isinstance(doc, Document):
                raise ValueError(f"没有找到id：{_id} 的文档")
            docs.append((doc, scores[0][j]))
        return docs

    def similarity_search_with_score(
        self, query: str, k: int = 4
    ) -> List[Tuple[Document, float]]:
        embedding = self.embedding_function(query)
        docs = self.similarity_search_with_score_by_vector(embedding, k)
        return docs
    
    def similarity_search_by_vector(
        self, embedding: List[float], k: int = 4
    ) -> List[Document]:
        docs_and_scores = self.similarity_search_with_score_by_vector(embedding, k)
        return [doc for doc, _ in docs_and_scores]
    
    def similarity_search(
        self, query: str, k: int = 4
    ) -> List[Document]:
        docs_and_scores = self.similarity_search_with_score(query, k)
        return [doc for doc, _ in docs_and_scores]
    

    @classmethod
    def __from(
        cls,
        texts: List[str],
        embeddings: List[List[float]],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None
    ) -> FAISS:
        faiss = dependable_faiss_import()
        index = faiss.IndexFlatL2(len(embeddings[0]))
        index.add(np.array(embeddings, dtype=np.float32))
        documents = []
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            documents.append(Document(page_content=text, metadata=metadata))
        index_to_id = {i: str(uuid.uuid4()) for i in range(len(documents))}
        docstore = InMemoryDocstore(
            {index_to_id[i]: doc for i, doc in enumerate(documents)}
        )
        return cls(embedding.embed_query, index, docstore, index_to_id)
    
    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        **kwargs
    ) -> FAISS:
        embeddings = embedding.embed_documents(texts)
        return cls.__from(texts, embeddings, embedding, metadatas, **kwargs)