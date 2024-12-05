
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel

from eve.schema import BaseMemory


class Chain(BaseModel, ABC):

    memory: Optional[BaseMemory] = None

    @property
    @abstractmethod
    def input_keys(self) -> List[str]:
        """该chain 需要的输入 key"""
    
    @property
    @abstractmethod
    def output_keys(self) -> List[str]:
        """该chain 需要的输出 key"""
    
    @abstractmethod
    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        """根据输入获取输出结果，由子类实现"""
    
    def __call__(self, inputs: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
        inputs = self.prep_inputs(inputs)
        try:
            outputs = self._call(inputs)
        except (KeyboardInterrupt, Exception) as e:
            raise e
        return self.prep_outputs(inputs, outputs)

    def prep_inputs(self, inputs: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
        if not isinstance(inputs, dict):
            _input_keys = set(self.input_keys)
            if self.memory is not None:
                _input_keys = _input_keys.difference(self.memory.memory_variables)
                if len(_input_keys) != 1:
                    raise ValueError(
                        "如果仅有一个字符串输入，且该chain期望有多个输入，那么需要字典格式的输入"
                    )
            inputs = {list(_input_keys)[0]: inputs}
        if self.memory is not None:
            external_context = self.memory.load_memory_variables
            inputs = dict(inputs, **external_context)
        return inputs
    
    def prep_outputs(
        self,
        inputs: Dict[str, str],
        outputs: Dict[str, str]
    ) -> Dict[str, str]:
        if self.memory is not None:
            self.memory.save_context(inputs, outputs)
        return outputs

    def run(self, *args: Any, **kwargs: Any) -> str:
        if len(self.output_keys) != 1:
            raise ValueError(
                "`run`方法仅支持单个输出key"
            )
        if args and not kwargs:
            if len(args) != 1:
                raise ValueError(
                    "`run` 方法仅支持单个位置参数"
                )
            return self(args[0])[self.output_keys[0]]
        
        if kwargs and not args:
            return self(kwargs)[self.output_keys[0]]
        raise ValueError(
            "不支持该类型参数"
        )
