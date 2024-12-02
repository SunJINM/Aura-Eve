
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
from pydantic import BaseModel


class Chain(BaseModel, ABC):

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
            output = self._call(inputs)
        except (KeyboardInterrupt, Exception) as e:
            raise e
        return output

    def prep_inputs(self, inputs: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
        if not isinstance(inputs, dict):
            _input_keys = set(self.input_keys)
            if len(_input_keys) != 1:
                raise ValueError(
                    "单个值被输入，必须chain的input_key为一个"
                )
            inputs = {list(_input_keys)[0]: inputs}
        return inputs

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
