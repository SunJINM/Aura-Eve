
from abc import ABC
from typing import Union

from eve.schema import Document


class Docstore(ABC):

    def search(self, search: str) -> Union[str, Document]:
        """"""