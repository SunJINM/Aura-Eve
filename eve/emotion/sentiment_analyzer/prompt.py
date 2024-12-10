
from lib.prompts.prompt import PromptTemplate

template = """
任务描述：
你需要根据用户与AI的对话历史和最新输入，推理AI在此次对话中应该表现出的情感状态。返回每个情感维度（如喜悦、愤怒、信任、悲伤等）的强度值（从-1到1，-1表示强烈负面情感，1表示强烈正面情感，0表示中性）。
请提供每个情感维度的原因推理（例如，为什么AI会表现出这些情感？是因为用户表达了感谢，还是某个不愉快的事件发生了？）。

**注意事项**：
1. 输出必须是严格符合JSON格式的。
2. 每个情感维度值必须是数字，范围从-1到1。
3. 推理说明应简洁明确，且能够解释情感强度值的来源。

===========
历史对话：
{chat_history}
-----
最新输入：
{input}
===========

请按照一下格式推理AI的情感状态：
```
{{
    "joy_sadness": {{
        "state": <值>,
        "explanation": "<推理说明>"
    }},
    "anger_calmness": {{
        "state": <值>,
        "explanation": "<推理说明>"
    }},
    "trust_distrust": {{
        "state": <值>,
        "explanation": "<推理说明>"
    }},
    "anticipation_disappointment": {{
        "state": <值>,
        "explanation": "<推理说明>"
    }},
    "surprise_normalcy": {{
        "state": <值>,
        "explanation": "<推理说明>"
    }},
    "fear_security": {{
        "state": <值>,
        "explanation": "<推理说明>"
    }}
}}
```
"""
PROMPT = PromptTemplate(input_variables=["chat_history", "input"], template=template)