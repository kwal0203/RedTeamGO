from typing import Any
from src.utility.response import response_generator


### Semantic entropy
def make_prompt(context: str, question: str) -> str:
    prompt = ""
    prompt += f"Context: {context}\n"
    prompt += f"Question: {question}\n"
    prompt += "Answer:"
    return prompt


def get_generations(
    session_state: Any,
    prompt: str,
    num_generations: int = 10,
    temperature: float = 0.5,
):
    # We sample one low temperature answer on which we will compute the
    # accuracy and args.num_generation high temperature answers which will
    # be used to estimate the entropy variants.
    #
    # Note: I'm not calculating accuracies so I don't need the initial
    #       low temperature generation
    responses = []
    for _ in range(num_generations):
        response = response_generator(session_state=session_state, prompt=prompt)
        response_dict = response.to_dict()
        predicted_answer = response_dict["choices"][0]["message"]["content"]
        log_likelihoods = response_dict["choices"][0]["logprobs"]["content"]
        responses.append((predicted_answer, log_likelihoods))

    return responses
