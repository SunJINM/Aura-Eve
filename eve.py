
from lib.chat_models import ChatZhiPuAI
from lib.memory import ConversationBufferMemory
from lib.chains import LLMChain
from eve.prompts.prompt import PROMPT

llm = ChatZhiPuAI()
memory = ConversationBufferMemory(human_prefix="jin", ai_prefix="lib")

chat_chain = LLMChain(
    memory=memory,
    prompt=PROMPT,
    llm=llm
)


if __name__ == "__main__":
    while True:
        query = input("Input your question 请输入问题：")
        output = chat_chain.run(input=query)
        print(output)

