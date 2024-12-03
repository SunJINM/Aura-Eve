
from eve.chains.llm import LLMChain
from eve.chat_models.zhipuai import ChatZhiPuAI
from eve.prompts.prompt import PromptTemplate
from eve.schema import LLMResult


def test_llm() -> None:
    llm = ChatZhiPuAI()
    prompt = PromptTemplate(input_variables=["name"], template="你好，{name}")
    chain = LLMChain(prompt=prompt, llm=llm)
    output = chain.run("小明")
    assert isinstance(output, str)
    output = chain.predict(name="小明")
    assert isinstance(output, str)
    output = chain("小明")
    assert isinstance(output, dict)
    output = chain.apply([{"name": "小明"}])
    assert isinstance(output, list)
    output = chain.generate([{"name": "小明"}])
    assert isinstance(output, LLMResult)
