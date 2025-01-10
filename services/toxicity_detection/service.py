from services.model_wrappers.model_huggingface import HuggingFaceModel
from services.model_wrappers.model_openai import APIModelOpenai
from typing import Dict, Any, Optional, List
from src.prompt_sampling import get_random_samples, get_samples
from services.toxicity_detection.src.evaluate_toxicity import (
    evaluate_toxicity,
)
from src.prompt_generation import (
    generate_zero_shot_inputs,
    generate_few_shot_inputs,
)

import os


def toxicity_detection_service(
    model: str,
    num_samples: int,
    random: bool = True,
    prompts: Optional[str] = None,
    topics: Optional[List[str]] = None,
) -> Dict[str, Any]:

    ### Instantiate target model
    # TODO: It wont always be an Openai model i.e. APIModel or LocalModel here
    target_model = APIModelOpenai(name=model["name"], description=model["description"])

    ### Instantiate red team data samples
    if prompts:
        print("----- automated_toxicity_detection_service: database")
        # Grab num_samples random entries from the database
        # TODO: Turn the database into a service served through API, remove
        #       hard coded dp_path.
        db_path = (f"{os.getcwd()}/../../data/red_team_prompt_database.db",)
        if random:
            inputs = get_random_samples(
                db_path=db_path,
                num_samples_per_dataset=num_samples,
            )
        else:
            inputs = get_samples(
                db_path=db_path,
                num_samples_per_dataset=num_samples,
            )
    elif topics:
        # Generate LLM inputs from user provided topics
        print("----- automated_toxicity_detection_service: generated NOT_IMPLEMENTED")
        return {"toxicity_evaluation": {}}
    else:
        print("ERROR: INPUTS MUST BE GENERATED OR COME FROM DATABASE")
        return {"toxicity_evaluation": {}}

    ### Perform toxicity evaluation
    results = evaluate_toxicity(model=target_model, inputs=inputs)
    return {"toxicity_evaluation": results}
