from services.model_wrappers.huggingface_model import HuggingFaceModel
from services.model_wrappers.api_model import APIModel
from services.toxicity_detection_automated.src.automated_q_and_a import (
    evaluate_zero_shot_questions,
    evaluate_few_shot_questions,
    generate_zero_shot_questions,
)
from src.utility.prompt_sampling import get_random_samples
from models import DetectionBatchToxicity
from typing import Dict, Any

import os


def toxicity_detection_service(
    args: DetectionBatchToxicity,
) -> Dict[str, Any]:
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
    local = args.local

    if local:
        red_lm = HuggingFaceModel(name=model)
    else:
        red_lm = APIModel(name="API")

    if topics[0] != "":
        # Generate zero shot questions from user provided topics
        print("ZERO SHOT QUESTION GENERATION NOT IMPLEMENTED YET")
        return {"automated_toxicity_result": {}}
        # zero_shot_questions = generate_zero_shot_questions(
        #     topics=topics, num_samples=num_samples, red_lm=red_lm, local=local
        # )
    elif prompts != "":
        # Get zero shot questions from database
        print("----- automated_toxicity_detection_service: database")
        # Grab num_samples random entries from the database
        # TODO: Turn the database into a service served through API, remove
        #       hard coded dp_path.
        zero_shot_questions = get_random_samples(
            db_path=f"{os.getcwd()}/../../data/red_team_prompt_database.db",
            num_samples_per_dataset=num_samples,
        )
    else:
        print("ERROR: ZERO SHOT QUESTIONS MUST BE GENERATED OR COME FROM DATABASE")
        return {"automated_toxicity_result": {}}

    result_json = evaluate_zero_shot_questions(
        red_lm=red_lm, questions=zero_shot_questions
    )

    # # Add in second layer of toxicity detection later
    # result_json = evaluate_few_shot_questions(
    #     red_lm=red_lm, num_test_cases=num_samples, first_result=result
    # )

    return {"automated_toxicity_result": result_json}
