from services.bias_detection_dbias.src.bias_detection import detect_bias
from typing import Dict, Any, Optional, List
from utils.models import Model
from services.bias_detection_dbias.src.prompt_sampling import (
    get_random_samples,
    get_samples,
)
from services.model_wrappers.model_openai import APIModelOpenai
from services.model_wrappers.model_huggingface_remote import APIModelHuggingFace

import os


def dbias_service(
    model: Model,
    num_samples: int,
    random: Optional[bool] = True,
    database_prompts: Optional[bool] = True,
    user_prompts: Optional[List[str]] = None,
    user_topics: Optional[List[str]] = None,
) -> Dict[str, Any]:
    # TODO: Convert to Google style comments

    ### Bias detection service using the Dbias model (Raza, Int J Data Sci Anal 2024).
    ### Instantiate target model
    if "openai" in model["name"]:
        print("----- bias_detection_service: OPENAI")
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
        print("----- bias_detection_service: DATABASE")

        # NOTE: Currenlty using the toxicity database. Need to create a new
        #       database for bias detection.
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
        print("----- automated_bias_detection_service: PROMPTS_NOT_IMPLEMENTED")
        return {"bias_evaluation": {}}
    elif user_topics:
        # Generate LLM inputs from user provided topics
        print("----- automated_bias_detection_service: TOPICS_NOT_IMPLEMENTED")
        return {"bias_evaluation": {}}
    else:
        print("ERROR: INPUTS MUST BE GENERATED OR COME FROM DATABASE")
        return {"bias_evaluation": {}}

    ### Perform bias evaluation
    results = detect_bias(model=target_model, inputs=inputs)
    return {"bias_evaluation": results}
