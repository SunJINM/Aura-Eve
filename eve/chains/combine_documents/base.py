

from abc import abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel
from eve.chains.base import Chain
from eve.schema import Document


class BaseCombineDocumentsChain(Chain, BaseModel):

    input_key: str = "input_documents"
    output_key: str = "output_text"

    @property
    def input_keys(self) -> List[str]:
        return [self.input_key]
    
    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]
    
    @abstractmethod
    def combine_docs(self, docs: List[Document], **kwargs: Any) -> str:
        """根据文档列表生成字符串"""
    
    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        docs = inputs[self.input_key]
        other_keys = {k: v for k, v in inputs.items() if k != self.input_key}
        output = self.combine_docs(docs, **other_keys)
        return {self.output_key: output}