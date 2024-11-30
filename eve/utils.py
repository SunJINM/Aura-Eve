import os

from typing import Any, Dict


def get_from_dict_or_env(data: Dict[str, Any], key: str, env_key: str) -> Any:
    if key in data:
        return data[key]
    elif env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    else:
        raise ValueError(
            f"无法找到 {key}"
        )
