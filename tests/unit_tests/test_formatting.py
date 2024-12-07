import pytest

from lib.formatting import formatter

def test_valid_formatting() -> None:
    
    template = "这是一个{foo}的测试"
    output = formatter.format(template, foo="正确")
    expected_output = "这是一个正确的测试"
    assert output == expected_output

def test_does_not_allow_args() -> None:
    template = "这是一个{foo}的测试"
    with pytest.raises(ValueError):
        formatter.format(template, "正确的")


def test_does_not_allow_extra_kwargs() -> None:
    template = "这是一个{foo}的测试"
    with pytest.raises(KeyError):
        formatter.format(template, foo="正确的", bar="错误的")