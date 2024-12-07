
from lib.prompts.prompt import PromptTemplate

def test_prompt_valid() -> None:
    template = "这是一个{foo}的测试"
    input_variables = ["foo"]
    prompt = PromptTemplate(input_variables=input_variables, template=template)
    assert prompt.input_variables == input_variables
    assert prompt.template == template
