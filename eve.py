
from typing import List
from eve.llms import ZhiPuAI
from eve.prompts.chat import ChatPromptTemplate
from eve.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage

llm = ZhiPuAI()


def get_answer(chat_history: List[BaseMessage]) -> str:

    prompt_template = ChatPromptTemplate.from_messages(chat_history)
    prompt = prompt_template.format()
    return llm.generate(prompt=prompt)


if __name__ == "__main__":
    history_messages: List[BaseMessage] = [SystemMessage(content="你现在要扮演我的女友，今年18岁，叫eve。")]
    while True:
        query = input("Input your question 请输入问题：")
        history_messages.append(HumanMessage(content=query))
        print(history_messages)
        output = get_answer(chat_history=history_messages)
        history_messages.append(AIMessage(content=output))
        print(output)

