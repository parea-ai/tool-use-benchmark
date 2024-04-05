from openai import AsyncOpenAI
from parea import Parea, trace

from constants import GORILLA_TO_OPENAPI
from evals.ast_checker import ast_check_eval
from inference.utils import augment_prompt_by_languge, language_specific_pre_processing, convert_to_tool


def create_call_openai(p: Parea, model_name: str) -> callable:
    client = AsyncOpenAI()
    p.wrap_openai_client(client)

    @trace(eval_funcs=[ast_check_eval])
    async def call_openai(question: str, function: list | dict | str, test_category: str):
        prompt = augment_prompt_by_languge(question, test_category)
        if isinstance(function, (dict, str)):
            function = [function]
        functions = language_specific_pre_processing(function, test_category, True)
        if type(functions) is not list:
            functions = [functions]
        message = [{"role": "user", "content": "Questions:" + prompt}]
        oai_tool = convert_to_tool(
            functions, GORILLA_TO_OPENAPI, 'openai', test_category, True
        )

        response = await client.chat.completions.create(
            messages=message,
            model=model_name,
            temperature=0.7,
            max_tokens=1200,
            top_p=1.0,
            tools=oai_tool,
        )
        try:
            result = [
                {func_call.function.name: func_call.function.arguments}
                for func_call in response.choices[0].message.tool_calls
            ]
        except:
            result = response.choices[0].message.content
        return result

    return call_openai
