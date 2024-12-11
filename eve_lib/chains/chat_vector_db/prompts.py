
from eve_lib.prompts.prompt import PromptTemplate


_template = """任务：给一段对话和一个后续问题，将后续问题改写为一个独立的、完善的问题。确保问题是完整的，没有模糊指代。
-----------------
聊天记录：
{chat_history}
-----------------
后续问题：{question}
-----------------
改写后的独立、完整的问题："""

CONDESE_PROMPT_TEMPLATE = PromptTemplate.from_template(_template)

prompt_template = """基于以下内容，简洁和专业的回答用户的问题。
如果无法从中得到答案，请说 "不知道，没有足够相关信息"，不要试图编造答案。答案请使用中文。
-----------------
{context}
-----------------
问题：{question}
-----------------
有用的回答："""
QA_PROMPT = PromptTemplate.from_template(prompt_template)