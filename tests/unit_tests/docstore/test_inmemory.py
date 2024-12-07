
from lib.docstore.in_memory import InMemoryDocstore
from lib.schema import Document


def test_document_found() -> None:
    _dict = {"foo": Document(page_content="bar")}
    docstore = InMemoryDocstore(_dict)
    output = docstore.search("foo")
    assert isinstance(output, Document)
    assert output.page_content == "bar"

