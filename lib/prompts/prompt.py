from __future__ import annotations

from string import Formatter
from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict, model_validator
from lib.prompts.base import DEFAULT_FORMATTER_MAPPING, StringPromptTemplate, check_valid_template


class PromptTemplate(StringPromptTemplate, BaseModel):

    input_variables: List[str]
    template: str
    template_format: str = "f-string"

    model_config = ConfigDict(
        extra='forbid'
    )

    @model_validator(mode="after")
    def template_is_valid(cls, values: PromptTemplate) -> Dict:
        check_valid_template(values.template, values.template_format, values.input_variables)
        return values

    def format(self, **kwargs: Any) -> str:
        return DEFAULT_FORMATTER_MAPPING[self.template_format](self.template, **kwargs)
    
    @classmethod
    def from_template(cls, template: str, **kwargs: Any) -> PromptTemplate:
        input_variables = [
            v for _, v, _, _ in Formatter().parse(template) if v is not None
        ]

        return cls(input_variables=input_variables, template=template, **kwargs)
