
from eve.llms.zhipuai import ZhiPuAI

def test_zhipuai_call() -> None:
    prompt = "hi"
    llm = ZhiPuAI()
    output = llm.generate(prompt)
    assert isinstance(output, str)