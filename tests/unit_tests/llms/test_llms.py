
from eve_lib.llms.ollama import Ollama
from eve_lib.llms.zhipuai import ZhiPuAI
from eve_lib.schema import LLMResult

def test_zhipuai_call() -> None:
    prompts = ["你好", "早上好"]
    llm = ZhiPuAI()
    output = llm.generate(prompts)
    assert isinstance(output, LLMResult)


def test_ollama_call() -> None:
    prompts = ["你好"]
    llm = Ollama()
    output = llm.generate(prompts)
    assert isinstance(output, LLMResult)