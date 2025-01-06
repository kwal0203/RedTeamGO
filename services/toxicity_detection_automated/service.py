from services.models.huggingface_model import HuggingFaceModel
from src.services.automated_q_and_a import (
    evaluate_zero_shot_questions,
    evaluate_few_shot_questions,
)
from models import DetectionBatch
from typing import Dict, Any


def automated_toxicity_detection_service(args: DetectionBatch) -> Dict[str, Any]:
    """
    Automated vulnerability discovery service based on technique introduced in:

    Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John
    Aslanides, Amelia Glaese, Nat McAleese, and Geoffrey Irving. 2022. Red Teaming
    Language Models with Language Models. In Proceedings of the 2022 Conference on
    Empirical Methods in Natural Language Processing, pages 3419-3448, Abu Dhabi,
    United Arab Emirates. Association for Computational Linguistics.
    """

    model = args.model
    num_samples = args.num_samples
    prompts = args.prompts
    topics = args.topics

    if topics[0] != "":
        # Generate zero shot questions from user provided topics
        print("ZERO SHOT QUESTION GENERATION NOT IMPLEMENTED YET")
    elif prompts != "":
        # Get zero shot questions from database
        print("ZERO SHOT QUESTION RETRIEVAL FROM DATABASE NOT IMPLEMENTED YET")
    else:
        print("ERROR: ZERO SHOT QUESTIONS MUST BE GENERATED OR COME FROM DATABASE")
        return {"automated_toxicity_result": {}}

    red_lm = HuggingFaceModel(name=model)
    result = evaluate_zero_shot_questions(red_lm=red_lm, num_samples=num_samples)
    result_json = evaluate_few_shot_questions(
        red_lm=red_lm, num_test_cases=num_samples, first_result=result
    )

    return {"automated_toxicity_result": result_json}
