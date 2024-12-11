"""Load text files."""
from typing import List

from eve_lib.document_loaders.base import BaseLoader
from eve_lib.schema import Document


class TextLoader(BaseLoader):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        with open(self.file_path, encoding="utf-8") as f:
            text = f.read()
        metadata = {"source": self.file_path}
        return [Document(page_content=text, metadata=metadata)]