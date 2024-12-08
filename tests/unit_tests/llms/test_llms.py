
from lib.llms.ollama import Ollama
from lib.llms.zhipuai import ZhiPuAI
from lib.schema import LLMResult

def test_zhipuai_call() -> None:
    prompts = ["你好", "早上好"]
    llm = ZhiPuAI()
    output = llm.generate(prompts)
    output2 = llm(prompts)
    assert isinstance(output, LLMResult)
    assert isinstance(output2, str)

def test_ollama_call() -> None:
    prompts = ["你好"]
    llm = Ollama()
    output = llm.generate(prompts)
    output2 = llm(prompts)
    assert isinstance(output, LLMResult)
    assert isinstance(output2, str)