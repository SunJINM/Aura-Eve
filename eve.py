
from lib.chat_models import ChatZhiPuAI
from lib.memory import ConversationBufferMemory
from lib.chains import LLMChain
from lib.output_parsers import RegexParser
from eve.prompts.prompt import PROMPT

llm = ChatZhiPuAI()
memory = ConversationBufferMemory(human_prefix="Jin", ai_prefix="eve")

chat_chain = LLMChain(
    memory=memory,
    prompt=PROMPT,
    llm=llm
)

parser = RegexParser(regex=r"(.*?)（(.*?)）：(.*)", output_keys=["name", "mode", "content"], default_output_key="content")


if __name__ == "__main__":
    while True:
        query = input("请输入问题：")
        output = chat_chain.run(input=query)
        res = parser.parse(output)
        print(f"{res['name']}:{res['content']}")

