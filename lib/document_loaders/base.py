
from abc import ABC, abstractmethod
from typing import List

from lib.schema import Document


class BaseLoader(ABC):

    @abstractmethod
    def load(self) -> List[Document]:
        """加载数据到文档中"""