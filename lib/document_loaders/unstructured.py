
from abc import ABC, abstractmethod
from fileinput import filename
from typing import Any, List
from lib.document_loaders.base import BaseLoader
from lib.schema import Document


class UnstructuredBaseLoader(BaseLoader, ABC):

    def __init__(self, mode: str = "single", **unstructured_kwargs: Any):
        try:
            import unstructured
        except ImportError:
            raise ValueError(
                "无法找到 unstructured 模块"
            )
        _valid_modes = {"single", "elements"}
        if mode not in _valid_modes:
            raise ValueError("mode: {mode} 应该是 {_valid_modes} 中的一个")
        self.mode = mode

        self.unstructured_kwargs = unstructured_kwargs


    @abstractmethod
    def _get_elements(self) -> List:
        """"""

    @abstractmethod
    def _get_metadata(self) -> List:
        """"""

    def load(self) -> List[Document]:
        elements = self._get_elements()
        if self.mode == "elements":
            docs: List[Document] = list()
            for element in elements:
                metadata = self._get_metadata()
                if hasattr(element, "metadata"):
                    metadata.update(element.metadata.to_dict())
                if hasattr(element, "category"):
                    metadata["category"] = element.category
                docs.append(Document(page_content=str(element), metadata=metadata))
        elif self.mode == "single":
            metadata = self._get_metadata()
            text = "\n\n".join([str(el) for el in elements])
            docs = [Document(page_content=text, metadata=metadata)]
        else:
            raise ValueError("不支持模式{self.mode}")
        return docs
    
class UnstructuredFileLoader(UnstructuredBaseLoader):

    def __init__(
        self, file_path: str, mode: str = "single", **unstructured_kwargs: Any
    ):
        self.file_path = file_path
        super().__init__(mode=mode, **unstructured_kwargs)
    
    def _get_elements(self) -> List:
        from unstructured.partition.auto import partition
        return partition(filename=self.file_path, **self.unstructured_kwargs)
    
    def _get_metadata(self) -> List:
        return {"source": self.file_path}