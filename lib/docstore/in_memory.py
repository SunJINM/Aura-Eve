

from typing import Dict, Union
from lib.docstore.base import Docstore
from lib.schema import Document


class InMemoryDocstore(Docstore):

    def __init__(self, _dict: Dict[str, Document]):
        self._dict = _dict

    def search(self, search: str) -> Union[str, Document]:
        if search in self._dict:
            return self._dict[search]
        else:
            return f"ID {search} not found"