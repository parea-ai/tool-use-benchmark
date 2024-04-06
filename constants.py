SYSTEM_PROMPT_FOR_CHAT_MODEL = """"
    You are an expert in composing functions. You are given a question and a set of possible functions. 
    Based on the question, you will need to make one or more function/tool calls to achieve the purpose. 
    If none of the function can be used, point it out. If the given question lacks the parameters required by the function,
    also point it out. You should only return the function call in tools call sections.
    """

USER_PROMPT_FOR_CHAT_MODEL = """
    Questions:{user_prompt}\nHere is a list of functions in JSON format that you can invoke:\n{functions}. 
    Should you decide to return the function call(s),Put it in the format of [func1(params_name=params_value, params_name2=params_value2...), func2(params)]\n
    NO other text MUST be included. 
"""
GORILLA_TO_OPENAPI = {
    "integer": "integer",
    "number": "number",
    "float": "number",
    "string": "string",
    "boolean": "boolean",
    "bool": "boolean",
    "array": "array",
    "list": "array",
    "dict": "object",
    "object": "object",
    "tuple": "array",
    "any": "string",
    "byte": "integer",
    "short": "integer",
    "long": "integer",
    "double": "number",
    "char": "string",
    "ArrayList": "array",
    "Array": "array",
    "HashMap": "object",
    "Hashtable": "object",
    "Queue": "array",
    "Stack": "array",
    "Any": "string",
    "String": "string",
    "Bigint": "integer",
}

GORILLA_TO_PYTHON = {
    "integer": "int",
    "number": "float",
    "float": "float",
    "string": "str",
    "boolean": "bool",
    "bool": "bool",
    "array": "list",
    "list": "list",
    "dict": "dict",
    "object": "dict",
    "tuple": "tuple",
    "any": "str",
    "byte": "int",
    "short": "int",
    "long": "int",
    "double": "float",
    "char": "str",
    "ArrayList": "list",
    "Array": "list",
    "HashMap": "dict",
    "Hashtable": "dict",
    "Queue": "list",
    "Stack": "list",
    "Any": "str",
    "String": "str",
    "Bigint": "int",
}

# supported open source models
MODEL_ID_DICT = {
    "deepseek-7b": "deepseek-coder",
    "glaiveai": "vicuna_1.1",
    "llama-v2-7b": "llama-2",
    "llama-v2-13b": "llama-2",
    "llama-v2-70b": "llama-2",
    "dolphin-2.2.1-mistral-7b": "dolphin-2.2.1-mistral-7b",
    "gorilla-openfunctions-v0": "gorilla",
    "functionary-small-v2.2": "mistral",
    "functionary-medium-v2.2": "mistral",
}

JAVA_TYPE_CONVERSION = {
    "byte": int,
    "short": int,
    "integer": int,
    "number": float,
    "float": float,
    "double": float,
    "long": int,
    "boolean": bool,
    "char": str,
    "object": dict,
    "Array": list,
    "array": list,
    "ArrayList": list,
    "Set": set,
    "HashMap": dict,
    "Hashtable": dict,
    "Queue": list,  # this can be `queue.Queue` as well, for simplicity we check with list
    "Stack": list,
    "String": str,
    "string": str,
    "any": str,
}

JS_TYPE_CONVERSION = {
    "String": str,
    "string": str,
    "integer": int,
    "float": float,
    "number": float,
    "Bigint": int,
    "Boolean": bool,
    "dict": dict,
    "object": dict,
    "array": list,
    "any": str,
}

UNDERSCORE_TO_DOT = [
    "gpt-4-1106-preview-FC",
    "gpt-4-0125-preview-FC",
    "gpt-4-0613-FC",
    "gpt-3.5-turbo-0125-FC",
    "mistral-large-2402-FC",
    "mistral-large-2402-FC-Any",
    "mistral-large-2402-FC-Auto",
    "mistral-small-2402-FC-Any",
    "mistral-small-2402-FC-Auto",
    "mistral-small-2402-FC",
    "gemini-1.0-pro",
    "meetkai/functionary-small-v2.2-FC",
    "meetkai/functionary-medium-v2.2-FC",
    "meetkai/functionary-small-v2.4-FC",
    "meetkai/functionary-medium-v2.4-FC",
]

TEST_CATEGORIES = {
    "executable_simple": "gorilla_openfunctions_v1_test_executable_simple.json",
    "executable_parallel_function": "gorilla_openfunctions_v1_test_executable_parallel_function.json",
    "executable_multiple_function": "gorilla_openfunctions_v1_test_executable_multiple_function.json",
    "executable_parallel_multiple_function": "gorilla_openfunctions_v1_test_executable_parallel_multiple_function.json",
    "simple": "gorilla_openfunctions_v1_test_simple.json",
    "relevance": "gorilla_openfunctions_v1_test_relevance.json",
    "parallel_function": "gorilla_openfunctions_v1_test_parallel_function.json",
    "multiple_function": "gorilla_openfunctions_v1_test_multiple_function.json",
    "parallel_multiple_function": "gorilla_openfunctions_v1_test_parallel_multiple_function.json",
    "java": "gorilla_openfunctions_v1_test_java.json",
    "javascript": "gorilla_openfunctions_v1_test_javascript.json",
    "rest": "gorilla_openfunctions_v1_test_rest.json",
    "sql": "gorilla_openfunctions_v1_test_sql.json",
}
