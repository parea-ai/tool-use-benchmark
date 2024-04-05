import json
import os

from dotenv import load_dotenv
from parea import Parea

from inference.call_openai import create_call_openai

test_category = 'simple'
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

load_dotenv()

p = Parea(api_key=os.getenv("PAREA_API_KEY"), project_name="tool-calling-benchmark")


call_openai = create_call_openai(p, "gpt-4-0125-preview")
# call_openai = create_call_openai(p, "gpt-3.5-turbo-0125")

p.experiment(
    f'Category {test_category}',
    data,
    call_openai
).run()
