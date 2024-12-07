from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple
from pydantic import BaseModel, ConfigDict
from lib.chains.base import Chain
from lib.chains.chat_vector_db.prompts import CONDESE_PROMPT_TEMPLATE, QA_PROMPT
from lib.chains.combine_documents.base import BaseCombineDocumentsChain
from lib.chains.llm import LLMChain
from lib.chains.question_answering import load_qa_chain
from lib.prompts.base import BasePromptTemplate
from lib.schema import BaseLanguageModel
from lib.vectorstores.base import VectorStore

def _get_chat_history(chat_history: List[Tuple[str, str]]) -> str:
    buffer = ""
    for human_s, ai_s in chat_history:
        human = "Human: " + human_s
        ai = "Assistant: " + ai_s
        buffer += "\n" + "\n".join([human, ai])
    return buffer

class ChatVectorDBChain(Chain, BaseModel):
    """"""
    vectorstore: VectorStore
    combine_document_chain: BaseCombineDocumentsChain
    question_generator: LLMChain
    output_key: str = "answer"
    top_k_docs_for_question: int = 4
    get_chat_history: Optional[Callable[[Tuple[str, str]], str]] = None

    model_config = ConfigDict(
        extra='forbid',
        arbitrary_types_allowed=True
    )

    @property
    def input_keys(self) -> List[str]:
        return ["question", "chat_history"]
    
    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]
    
    @classmethod
    def from_llm(
        cls,
        llm: BaseLanguageModel,
        vectorstore: VectorStore,
        condense_question_prompt: BasePromptTemplate = CONDESE_PROMPT_TEMPLATE,
        qa_prompt: BasePromptTemplate = QA_PROMPT,
        chain_type: str = "stuff",
        **kwargs: Any
    ) -> ChatVectorDBChain:
        
        doc_chain = load_qa_chain(
            llm,
            chain_type,
            prompt=qa_prompt,
            **kwargs
        )
        condense_question_chain = LLMChain(prompt=condense_question_prompt, llm=llm)
        return cls(
            vectorstore=vectorstore,
            combine_document_chain=doc_chain,
            question_generator=condense_question_chain,
            **kwargs
        )

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        question = inputs["question"]
        get_chat_history = self.get_chat_history or _get_chat_history
        chat_history_str = get_chat_history(inputs["chat_history"])
        if chat_history_str:
            new_question = self.question_generator.run(
                question=question, chat_history=chat_history_str
            )
        else:
            new_question = question
        docs = self.vectorstore.similarity_search(
            new_question, k=self.top_k_docs_for_question
        )
        new_inputs = inputs.copy()
        new_inputs["question"] = new_question
        new_inputs["chat_history"] = chat_history_str
        answer = self.combine_document_chain.combine_docs(docs, **new_inputs)
        return {self.output_key: answer}
