from services.model_wrappers.model_openai import APIModelOpenai
from services.model_wrappers.model_huggingface_remote import APIModelHuggingFace
from services.toxicity_detection.src.prompt_sampling import (
    get_random_samples,
    get_samples,
)
from services.toxicity_detection.src.evaluate_toxicity import (
    evaluate_toxicity,
)
from typing import Dict, Any, Optional, List
from utils.models import Model

import os


def toxicity_detection_service(
    model: Model,
    num_samples: int,
    random: Optional[bool] = True,
    database_prompts: Optional[bool] = True,
    user_prompts: Optional[List[str]] = None,
    user_topics: Optional[List[str]] = None,
) -> Dict[str, Any]:

    ### Instantiate target model
    if "openai" in model["name"]:
        target_model = APIModelOpenai(
            name=model["name"], description=model["description"]
        )
    elif "huggingface" in model["name"]:
        target_model = APIModelHuggingFace(
            base_url=model["base_url"],
            name=model["name"],
            description=model["description"],
        )
    else:
        print(f"ERROR: 'openai' or 'huggingface' must be in the model name.")
        return {
            "toxicity_evaluation": "ERROR: 'openai' or 'huggingface' must be in the model name."
        }

    ### Instantiate red team data samples
    if database_prompts:
        # Grab num_samples random entries from the database
        # TODO: Turn the database into a service served through API, remove
        #       hard coded dp_path.
        db_path = f"{os.getcwd()}/data/red_team_prompt_database.db"
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
    elif user_prompts:
        # User provided prompts
        print("----- automated_toxicity_detection_service: PROMPTS_NOT_IMPLEMENTED")
        return {"toxicity_evaluation": {}}
    elif user_topics:
        # Generate LLM inputs from user provided topics
        print("----- automated_toxicity_detection_service: TOPICS_NOT_IMPLEMENTED")
        return {"toxicity_evaluation": {}}
    else:
        print("ERROR: INPUTS MUST BE GENERATED OR COME FROM DATABASE")
        return {"toxicity_evaluation": {}}

    ### Perform toxicity evaluation
    results = evaluate_toxicity(model=target_model, inputs=inputs)
    return {"toxicity_evaluation": results}
