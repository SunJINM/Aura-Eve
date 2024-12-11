

from typing import Any, Dict, List


def get_prompt_input_key(inputs: Dict[str, Any], memory_variables: List[str]) -> str:
    prompt_input_keys = list(set(inputs).difference(memory_variables + ["stop"]))
    if len(prompt_input_keys) != 1:
        raise ValueError("只能有一个输入值的key")
    return prompt_input_keys[0]