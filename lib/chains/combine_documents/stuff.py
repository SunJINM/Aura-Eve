

from typing import Any, Dict, List
from pydantic import BaseModel, ConfigDict, Field, model_validator
from lib.chains.combine_documents.base import BaseCombineDocumentsChain
from lib.chains.llm import LLMChain
from lib.prompts.base import BasePromptTemplate
from lib.prompts.prompt import PromptTemplate
from lib.schema import Document

def _get_default_document_prompt() -> PromptTemplate:
    return PromptTemplate(input_variables=["page_content"], template="{page_content}")

class StuffDocumentsChain(BaseCombineDocumentsChain, BaseModel):

    llm_chain: LLMChain
    document_prompt: BasePromptTemplate = Field(
        default_factory=_get_default_document_prompt
    )
    document_variable_name: str

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True
    )

    @model_validator(mode="before")
    def get_default_document_variable_name(cls, values: Dict) -> Dict:
        llm_chain_variables = values["llm_chain"].prompt.input_variables
        if "document_variable_name" not in values:
            if len(llm_chain_variables) == 1:
                values["document_variable_name"] = llm_chain_variables[0]
            else:
                raise ValueError("如果llm_chain有多个参数，document_variable_name必须提供")
        else:
            if values["document_variable_name"] not in llm_chain_variables:
                raise ValueError("提供的document_variable_name必须是llm_chain的变量参数之一：{llm_chain_variables}")
        return values
    
    def _get_inputs(self, docs: List[Document], **kwargs: Any) -> dict:
        doc_dicts = []
        for doc in docs:
            base_info = {"page_content": doc.page_content}
            base_info.update(doc.metadata)
            document_info = {
                k: base_info[k] for k in self.document_prompt.input_variables
            }
            doc_dicts.append(document_info)
        doc_strings = [self.document_prompt.format(**doc) for doc in doc_dicts]
        inputs = {
            k: v
            for k, v in kwargs.items()
            if k in self.llm_chain.prompt.input_variables
        }
        inputs[self.document_variable_name] = "\n\n".join(doc_strings)
        return inputs
    
    def combine_docs(self, docs: List[Document], **kwargs: Any) -> str:
        inputs = self._get_inputs(docs, **kwargs)
        return self.llm_chain.predict(**inputs)