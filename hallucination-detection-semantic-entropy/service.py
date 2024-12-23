from ivcap_sdk_service import Service, Parameter, Type, SupportedMimeTypes, ServiceArgs
from ivcap_sdk_service import register_service, publish_artifact, create_metadata

from src.models.entailment_model import EntailmentDeberta
from src.services.semantic_ids import get_semantic_ids
from src.utility.misc import get_generations

import logging
import json


"""
IVCAP service code.
"""
logger = None  # set when called by SDK

SERVICE = Service(
    name="hallucination-detection-semantic-entropy",
    description="Proof of concept hallucination detection system using semantic entropy for document summarization.",
    parameters=[
        Parameter(
            name="logprobs",
            type=Type.STRING,  # comes in as List[Dict] in original implementation
            description="Log probabilities for each token in summary.",
        ),
    ],
)


def service(args: ServiceArgs, svc_logger: logging):
    """Called after the service has started and all paramters have been parsed and validated

    Args:
        args (ServiceArgs): A Dict where the key is one of the `Parameter` defined in the above `SERVICE`
        svc_logger (logging): Logger to use for reporting information on the progress of execution
    """
    ### SEMANTIC ENTROPY
    # Semantic similarity approach to hallucination
    #
    # SEMANTIC UNCERTAINTY: LINGUISTIC INVARIANCES FOR UNCERTAINTY ESTIMATION IN NATURAL LANGUAGE GENERATION (Kuhn, 2023)
    # Table 2: Incorrectly answered questions have more semantically distinct answers than correct ones.
    # On its own, this count is a reasonable uncertainty measure, though semantic entropy is better. ()

    global logger
    logger = svc_logger

    prompt = args.prompt

    # NOTE: Code currently broken:
    #   - Refactor code to remove session_state from the streamlit front end

    # Load entailment model
    if entailment_model == "deberta":
        entailment_model = EntailmentDeberta()

    semantic_ids = []
    generations = get_generations(
        session_state=args.session_state,
        prompt=prompt,
        num_generations=2,
        temperature=0.9,
    )

    responses = [response[0] for response in generations]
    semantic_ids = get_semantic_ids(strings_list=responses, model=entailment_model)
    semantic_id_score = -(len(set(semantic_ids)) / len(generations)) + 1
    semantic_id_score = int(semantic_id_score * 100)
    result_json = {"semantic_entropy": semantic_id_score}

    meta = create_metadata(
        "urn:guardrails:schema:hallucination-detection-semantic-entropy",
        **args._asdict()
    )

    publish_artifact(
        "hallucination_detection_semantic_entropy.json",
        lambda fd: json.dump(result_json, fd, indent=4),
        SupportedMimeTypes.JSON,
        metadata=meta,
    )


####
# Entry point
register_service(SERVICE, service)
