

from string import Formatter
from typing import Any, Mapping, Sequence, Union


class StrictFormatter(Formatter):

    def check_unused_args(
            self, 
            used_args: Sequence[Union[int, str]], 
            args: Sequence[Any], 
            kwargs: Mapping[str, Any]
    ) -> None:
        extra = set(kwargs).difference(used_args)
        if extra:
            raise KeyError(extra)
        
    def vformat(
        self,
        format_string: str,
        args: Sequence[Any],
        kwargs: Mapping[str, Any]
    ) -> str:
        if len(args) > 0:
            raise ValueError(
                "不能使用位置参数"
            )
        return super().vformat(format_string, args, kwargs)
    

formatter = StrictFormatter()