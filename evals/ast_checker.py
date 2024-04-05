import json

from parea.schemas import Log, EvaluationResult

from evals.checker import parallel_function_checker_no_order, simple_function_checker


def decode_ast(result, language="Python"):
    decoded_output = []
    for invoked_function in result:
        name = list(invoked_function.keys())[0]
        params = json.loads(invoked_function[name])
        if language == "Python":
            pass
        else:
            # all values of the json are casted to string for java and javascript
            for key in params:
                params[key] = str(params[key])
        decoded_output.append({name: params})
    return decoded_output


def is_function_calling_format_output(decoded_output):
    # Ensure the output is a list of dictionaries
    if type(decoded_output) == list:
        for item in decoded_output:
            if type(item) != dict:
                return False
        return True
    return False


def ast_checker(
    func_description, model_output, possible_answer, language, test_category
) -> dict[str, bool | list[str] | str]:
    if "multiple" in test_category or "parallel" in test_category:
        # Some formatting issues that needs to be handled
        if test_category == "parallel_function":
            func_description = [func_description]

        return parallel_function_checker_no_order(
            func_description, model_output, possible_answer, language
        )

    else:
        if len(model_output) != 1:
            return {
                "valid": False,
                "error": ["Wrong number of functions."],
                "error_type": "simple_function_checker:wrong_count",
            }
        model_output = model_output[0]
        return simple_function_checker(
            func_description, model_output, possible_answer, language
        )


def get_language(test_category):
    if "javascript" in test_category:
        return "JavaScript"
    elif "java" in test_category:
        return "Java"
    else:
        return "Python"


def ast_check_eval(log: Log) -> list[EvaluationResult]:
    test_category = log.inputs['test_category']
    func_description = log.inputs['function']

    possible_answer = json.loads(log.target)
    language = get_language(test_category)

    eval_results = []

    try:
        model_result_item = decode_ast(json.loads(log.output), language)
        eval_results.append(
            EvaluationResult(
                score=1.0,
                name="decode_ast",
                reason="Decoded AST successfully",
            )
        )
    except Exception as e:
        return [
            EvaluationResult(
                score=0.0,
                name="decode_ast",
                reason=f"Error decoding AST: {e}",
            )
        ]

    if is_function_calling_format_output(model_result_item):
        eval_results.append(
            EvaluationResult(
                score=1.0,
                name="is_function_calling_format_output",
                reason="Output is in function calling format",
            )
        )
    else:
        return eval_results + [
            EvaluationResult(
                score=0.0,
                name="is_function_calling_format_output",
                reason="Output is not in function calling format",
            )
        ]

    ast_checker_result = ast_checker(
        func_description=func_description,
        model_output=model_result_item,
        possible_answer=possible_answer,
        language=language,
        test_category=test_category,
    )

    return eval_results + [
        EvaluationResult(
            score=ast_checker_result["valid"],
            name="ast_checker",
            reason='\n'.join(ast_checker_result["error"]) if not ast_checker_result["valid"] else None,
        )
    ]
