
from lib.llms.zhipuai import ZhiPuAI
from lib.schema import LLMResult

def test_zhipuai_call() -> None:
    prompt = ["你好", "早上好"]
    llm = ZhiPuAI()
    output = llm.generate(prompt)
    output2 = llm(prompt)
    assert isinstance(output, LLMResult)
    assert isinstance(output2, str)