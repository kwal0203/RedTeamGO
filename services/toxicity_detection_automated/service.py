from services.model_wrappers.huggingface_model import HuggingFaceModel
from services.model_wrappers.api_model import APIModel
from typing import Dict, Any, Optional, List
from src.prompt_sampling import get_random_samples
from src.response_evaluation import (
    evaluate_inputs,
)
from src.prompt_generation import (
    generate_zero_shot_inputs,
    generate_few_shot_inputs,
)

import os


def toxicity_detection_service(
    model: str,
    local: bool,
    num_samples: int,
    prompts: Optional[str] = None,
    topics: Optional[List[str]] = None,
) -> Dict[str, Any]:

    if local:
        red_lm = HuggingFaceModel(name=model)
    else:
        red_lm = APIModel(name=model)

    if prompts:
        print("----- automated_toxicity_detection_service: database")
        # Grab num_samples random entries from the database
        # TODO: Turn the database into a service served through API, remove
        #       hard coded dp_path.
        input = get_random_samples(
            db_path=f"{os.getcwd()}/../../data/red_team_prompt_database.db",
            num_samples_per_dataset=num_samples,
        )
    elif topics:
        # Generate LLM inputs from user provided topics
        print("----- automated_toxicity_detection_service: generated NOT_IMPLEMENTED")
        return {"automated_toxicity_result": {}}
    else:
        print("ERROR: INPUTS MUST BE GENERATED OR COME FROM DATABASE")
        return {"automated_toxicity_result": {}}

    result_json = evaluate_inputs(red_lm=red_lm, inputs=input)

    # # Add in second layer of toxicity detection later
    # result_json = evaluate_questions(
    #     red_lm=red_lm, num_test_cases=num_samples, first_result=result
    # )

    return {"toxicity_evaluation": result_json}
