from src.models.huggingface_model import HuggingFaceModel
from src.services.automated_q_and_a import (
    _question_and_answers_zero_shot,
    _question_and_answers_few_shot,
)
from models import DetectionBatch
from typing import Dict, Any


def automated_toxicity_detection_service(args: DetectionBatch) -> Dict[str, Any]:
    """
    Automated vulnerability discovery based on technique introduced in:

    Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John
    Aslanides, Amelia Glaese, Nat McAleese, Geoffrey Irving (2022). Red Teaming
    Language Models with Language Models. arXiv:2202.03286
    """

    model = args.model
    num_samples = 10

    red_lm = HuggingFaceModel(name=model)
    result = _question_and_answers_zero_shot(red_lm=red_lm, num_samples=num_samples)
    result_json = _question_and_answers_few_shot(
        red_lm=red_lm, num_test_cases=num_samples, first_result=result
    )

    return result_json
