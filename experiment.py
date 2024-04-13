import os

from dotenv import load_dotenv
from parea import Parea

from load_data import load_data
from inference.call_anthropic import create_call_anthropic
from inference.call_openai import create_call_openai


load_dotenv()

p = Parea(api_key=os.getenv("PAREA_API_KEY"), project_name="tool-calling-benchmark")


def benchmark_models_on_data(test_category: str, data: list[dict]):
    for model_name, create_fn in [
        ("gpt-3.5-turbo-0125", create_call_openai),
        ("gpt-4-0125-preview", create_call_openai),
        ("claude-3-haiku-20240307", create_call_anthropic),
        ("claude-3-opus-20240229", create_call_anthropic),
        ("gpt-4-turbo-2024-04-09", create_call_openai),
    ]:
        print(f'Running {model_name} on {test_category}...')
        llm_call = create_fn(p, model_name)
        p.experiment(
            f'{test_category} category',
            data,
            llm_call,
        ).run(model_name.replace('.', ''))


if __name__ == "__main__":
    categories = [
        'simple',
        'multiple_function',
        'parallel_function',
        'parallel_multiple_function',
        'java',
        'javascript',
    ]
    for category in categories:
        data = load_data(category)
        benchmark_models_on_data(category, data)
