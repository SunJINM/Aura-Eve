import re

from typing import Dict, List, Optional
from pydantic import BaseModel
from lib.schema import BaseOutputParser


class RegexParser(BaseOutputParser, BaseModel):
    regex: str
    output_keys: List[str]
    default_output_key: Optional[str] = None

    def parse(self, text: str) -> Dict[str, str]:
        
        match = re.search(self.regex, text)
        if match:
            return {k: match.group(i + 1) for i, k in enumerate(self.output_keys)}
        else:
            if self.default_output_key is None:
                raise ValueError(f"无法解析输入内容: {text}")
            else:
                return {
                    k: text if k == self.default_output_key else ""
                    for k in self.output_keys
                }
