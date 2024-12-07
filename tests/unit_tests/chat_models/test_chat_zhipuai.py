
from lib.chat_models.zhipuai import ChatZhiPuAI
from lib.schema import BaseMessage, HumanMessage

def test_chat_zhipuai() -> None:
    chat = ChatZhiPuAI()
    message = HumanMessage(content="你好")
    response = chat([message])
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)