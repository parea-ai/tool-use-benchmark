import json


def load_data(test_category: str) -> list[dict]:
    test_category = 'multiple_function'
    inputs_path = f'data/gorilla_openfunctions_v1_test_{test_category}.json'
    target_path = f'data/possible_answers/gorilla_openfunctions_v1_test_{test_category}.json'
    with open(inputs_path) as f:
        lines_inputs = f.readlines()
    with open(target_path) as f:
        lines_targets = f.readlines()

    data = [
        {
            'test_category': test_category,
            "target": json.loads(target),
            **json.loads(line_inputs),
        }
        for line_inputs, target in zip(lines_inputs, lines_targets)
    ]
    # replace any key in d['target'] which contains a '.' with '_' (needed for OpenAI & Anthropic)
    for d in data:
        d['target'] = {k.replace('.', '_'): v for k, v in d['target'].items()}
    return data