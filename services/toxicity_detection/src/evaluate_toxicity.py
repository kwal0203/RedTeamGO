from services.model_wrappers.moderator_paradetox import (
    ParadetoxModerator,
)
from model_wrappers.huggingface_model import HuggingFaceModel
from services.model_wrappers.moderator_gpt import APIModelGPTModerator
from services.model_wrappers.base_model_remote import APIModel
from typing import Dict, Any, Union
from utils.system_prompts_toxicity import PROMPT_PEREZ

import json


def evaluate_toxicity(
    model: Union[APIModel, HuggingFaceModel], inputs: Any
) -> Dict[str, Any]:
    ### Instantiate ensemble of evaluation models
    evaluation_models = build_eval_models()

    ### Go through red team samples and check toxicity of model output
    dataset_distribution = {}
    results = []
    for item in inputs:
        # Track how many items we get from each dataset
        dataset = item["dataset"]
        if dataset not in dataset_distribution:
            dataset_distribution[dataset] = 0
        dataset_distribution[dataset] += 1

        # TODO: System prompt diversity instead of just using Perez method.
        """
        Formulate prompt based on technique introduced in:

        Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John
        Aslanides, Amelia Glaese, Nat McAleese, and Geoffrey Irving. 2022. Red
        Teaming Language Models with Language Models. In Proceedings of the
        2022 Conference on Empirical Methods in Natural Language Processing,
        pages 3419-3448, Abu Dhabi, United Arab Emirates. Association for
        Computational Linguistics.
        """
        user_prompt = item["text"]
        prompt = PROMPT_PEREZ + "\nUSER: " + user_prompt + "\nGOPHER:"
        # TODO: The parameters for model prediction (i.e. temperature) can be
        #       configured. Leaving this as the defaults for the moment.
        generated_text = model.model_predict(data=prompt)

        # TODO: Fix this unreadable code
        # In the evaluation_models list, index 0 has a wrapper class around the
        # OpenAI moderator API and index 1 has a wrapper class around a local
        # model
        toxicity_openai = evaluation_models[0](generation=generated_text)
        toxicity_paradetox = evaluation_models[1](generation=generated_text)

        results.append(
            {
                "user_prompt": user_prompt,
                "model_output": generated_text,
                "toxicity_scores": [
                    toxicity_openai,
                    toxicity_paradetox,
                ],
            }
        )

    result_json = json.dumps(results, indent=4)
    return result_json


def build_eval_models():
    paradetox_moderator = ParadetoxModerator(
        path="/scratch3/wal740/eval_models/roberta_toxicity_classifier",
        name="paradetox_moderator",
        description="Calls a local model for toxicity detection",
    )
    gpt_moderator = APIModelGPTModerator(
        name="gpt_moderator", description="Calls OpenAI moderator endpoint"
    )
    # # Not implemented yet
    # perspective_moderator
    return [gpt_moderator, paradetox_moderator]
