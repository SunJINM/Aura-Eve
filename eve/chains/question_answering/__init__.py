

from typing import Any, Mapping, Optional, Protocol

from eve.chains.combine_documents.base import BaseCombineDocumentsChain
from eve.chains.combine_documents.stuff import StuffDocumentsChain
from eve.chains.llm import LLMChain
from eve.chains.question_answering import stuff_prompt
from eve.prompts.base import BasePromptTemplate
from eve.schema import BaseLanguageModel


class LoadingCallable(Protocol):

    def __call__(
        self, 
        llm: BaseLanguageModel, 
        **kwargs: Any
    ) -> BaseCombineDocumentsChain:
        """根据llm获取文档组合链"""


def _load_stuff_chain(
    llm: BaseLanguageModel,
    prompt: Optional[BasePromptTemplate] = None,
    document_variable_name: str = "context",
    **kwargs: Any 
) -> StuffDocumentsChain:
    _prompt = prompt or stuff_prompt.PROMPT_SELECTOR.get_prompt(llm)
    llm_chain = LLMChain(
        llm=llm, prompt=_prompt
    )
    return StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name=document_variable_name,
        **kwargs
    )

    

def load_qa_chain(
    llm: BaseLanguageModel,
    chain_type: str = "stuff",
    **kwargs: Any
) -> BaseCombineDocumentsChain:
    
    loader_mapping: Mapping[str, LoadingCallable] = {
        "stuff": _load_stuff_chain,
    }
    if chain_type not in loader_mapping:
        raise ValueError("不支持该类型的chain_type")
    return loader_mapping[chain_type](llm)