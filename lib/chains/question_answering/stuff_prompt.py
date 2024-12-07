

from lib.chains.prompt_selector import ConditionalPromptSelector, is_chat_model
from lib.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from lib.prompts.prompt import PromptTemplate
from lib.schema import SystemMessage


prompt_template = """基于以下文本内容回答用户的问题。如果无法从中获取答案，请回答 "不知道"，不要尝试编造答案。
-----------
{context}
-----------
问题：{question}
-----------
有用的回答："""

PROMPT = PromptTemplate.from_template(prompt_template)

system_template = """基于以下文本内容回答用户的问题。如果无法从中获取答案，请回答 "不知道"，不要尝试编造答案。
-----------
{context}
-----------
"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)

PROMPT_SELECTOR = ConditionalPromptSelector(
    default_prompt=PROMPT, conditionals=[(is_chat_model, CHAT_PROMPT)]
)

