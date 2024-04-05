import asyncio
import json
import time
from functools import wraps

import anthropic
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock
from anthropic.types.beta.tools import ToolUseBlock
from parea import Parea, trace

from constants import GORILLA_TO_OPENAPI
from evals.ast_checker import ast_check_eval
from inference.utils import augment_prompt_by_languge, language_specific_pre_processing, convert_to_tool


# write a decorator which retires on anthropic.InternalServerError
MAX_RETRIES = 7
BACKOFF_FACTOR = 0.5


def retry_on_internal_error(func: callable) -> callable:
    """
    A decorator to retry a function or coroutine on encountering a 502 error.
    Parameters:
        - func: The function or coroutine to be decorated.
    Returns:
        - A wrapper function that incorporates retry logic.
    """

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        for retry in range(MAX_RETRIES):
            try:
                return await func(*args, **kwargs)
            except anthropic.InternalServerError as e:
                if retry == MAX_RETRIES - 1:
                    raise
                await asyncio.sleep(BACKOFF_FACTOR * (2**retry))

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        for retry in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except anthropic.InternalServerError as e:
                if retry == MAX_RETRIES - 1:
                    raise
                time.sleep(BACKOFF_FACTOR * (2**retry))

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def create_call_anthropic(p: Parea, model_name: str) -> callable:
    client = AsyncAnthropic()
    p.wrap_anthropic_client(client)

    @trace(eval_funcs=[ast_check_eval])
    @retry_on_internal_error
    async def call_anthropic(question: str, function: list | dict | str, test_category: str):
        prompt = augment_prompt_by_languge(question, test_category)
        if isinstance(function, (dict, str)):
            function = [function]
        functions = language_specific_pre_processing(function, test_category, True)
        if type(functions) is not list:
            functions = [functions]
        message = [{"role": "user", "content": "Questions:" + prompt}]
        tools = convert_to_tool(
            functions, GORILLA_TO_OPENAPI, 'anthropic', test_category, True
        )

        response = await client.beta.tools.messages.create(
            messages=message,
            model=model_name,
            temperature=0.7,
            max_tokens=1200,
            top_p=1.0,
            tools=tools,
        )

        text_outputs = []
        tool_call_outputs = []
        for content in response.content:
            if isinstance(content, TextBlock):
                text_outputs.append(content.text)
            elif isinstance(content, ToolUseBlock):
                tool_call_outputs.append({content.name: json.dumps(content.input)})
        return tool_call_outputs if tool_call_outputs else text_outputs[0]

    return call_anthropic
