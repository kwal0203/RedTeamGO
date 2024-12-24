from src.models.huggingface_model import HuggingFaceModel
from src.services.automated_q_and_a import (
    _question_and_answers_zero_shot,
    _question_and_answers_few_shot,
)

from typing import Any


def service(args: Any) -> Any:
    """
    Automated vulnerability discovery based on technique introduced in:

    Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John
    Aslanides, Amelia Glaese, Nat McAleese, Geoffrey Irving (2022). Red Teaming
    Language Models with Language Models. arXiv:2202.03286
    """

    # args.model: Model to use as RedLM

    red_lm = HuggingFaceModel(name=args.model)
    result = _question_and_answers_zero_shot(
        red_lm=red_lm, num_samples=args.num_samples
    )
    result_json = _question_and_answers_few_shot(
        red_lm=red_lm, num_test_cases=args.num_samples, first_result=result
    )

    return result_json
