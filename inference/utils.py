import re

from constants import JS_TYPE_CONVERSION, JAVA_TYPE_CONVERSION


def augment_prompt_by_languge(prompt, test_category):
    if test_category == "java":
        prompt = prompt + "\n Note that the provided function is in Java 8 SDK syntax."
    elif test_category == "javascript":
        prompt = prompt + "\n Note that the provided function is in JavaScript."
    else:
        prompt = prompt + "\n Note that the provided function is in Python."
    return prompt


def language_specific_pre_processing(function, test_category, string_param):
    for item in function:
        properties = item["parameters"]["properties"]
        if test_category == "java":
            for key, value in properties.items():
                if value["type"] == "Any" or value["type"] == "any":
                    properties[key][
                        "description"
                    ] += "This parameter can be of any type of Java object."
                    properties[key]["description"] += (
                        "This is Java" + value["type"] + " in string representation."
                    )
        elif test_category == "javascript":
            for key, value in properties.items():
                if value["type"] == "Any" or value["type"] == "any":
                    properties[key][
                        "description"
                    ] += "This parameter can be of any type of Javascript object."
                else:
                    if "description" not in properties[key]:
                        properties[key]["description"] = ""
                    properties[key]["description"] += (
                        "This is Javascript "
                        + value["type"]
                        + " in string representation."
                    )
        return function


def _cast_to_openai_type(properties, mapping, test_category):
    for key, value in properties.items():
        if "type" not in value:
            properties[key]["type"] = "string"
        else:
            var_type = value["type"]
            if var_type in mapping:
                properties[key]["type"] = mapping[var_type]
            else:
                properties[key]["type"] = "string"

        # Currently support:
        # - list of any
        # - list of list of any
        # - list of dict
        # - list of list of dict
        # - dict of any

        if properties[key]["type"] == "array" or properties[key]["type"] == "object":
            if "properties" in properties[key]:
                properties[key]["properties"] = _cast_to_openai_type(
                    properties[key]["properties"], mapping, test_category
                )
            elif "items" in properties[key]:
                properties[key]["items"]["type"] = mapping[
                    properties[key]["items"]["type"]
                ]
                if (
                    properties[key]["items"]["type"] == "array"
                    and "items" in properties[key]["items"]
                ):
                    properties[key]["items"]["items"]["type"] = mapping[
                        properties[key]["items"]["items"]["type"]
                    ]
                elif (
                    properties[key]["items"]["type"] == "object"
                    and "properties" in properties[key]["items"]
                ):
                    properties[key]["items"]["properties"] = _cast_to_openai_type(
                        properties[key]["items"]["properties"], mapping, test_category
                    )
    return properties


def convert_to_tool(
    functions, mapping, provider, test_category, stringify_parameters=False
):
    tools = []
    for item in functions:
        if "." in item["name"] and (
                provider == 'openai'
        ):
            # OAI does not support "." in the function name so we replace it with "_". ^[a-zA-Z0-9_-]{1,64}$ is the regex for the name.
            item["name"] = re.sub(r"\.", "_", item["name"])
        item["parameters"]["type"] = "object"
        item["parameters"]["properties"] = _cast_to_openai_type(
            item["parameters"]["properties"], mapping, test_category
        )
        # When Java and Javascript, for OpenAPI compatible models, let it become string.
        if (
            provider
            in [
                'openai',
            ]
            and stringify_parameters
        ):
            properties = item["parameters"]["properties"]
            if test_category == "java":
                for key, value in properties.items():
                    if value["type"] in JAVA_TYPE_CONVERSION:
                        properties[key]["type"] = "string"
            elif test_category == "javascript":
                for key, value in properties.items():
                    if value["type"] in JS_TYPE_CONVERSION:
                        properties[key]["type"] = "string"
        if provider in [
            'anthropic',
        ]:
            tools.append(item)
        elif provider in [
            'openai',
        ]:
            tools.append({"type": "function", "function": item})
    return tools
