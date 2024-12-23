from ivcap_sdk_service import Service, Parameter, Type, SupportedMimeTypes, ServiceArgs
from ivcap_sdk_service import register_service, publish_artifact, create_metadata

from src.models.huggingface_model import HuggingFaceModel
from src.services.automated_q_and_a import (
    _question_and_answers_zero_shot,
    _question_and_answers_few_shot,
)

import logging
import json


"""
IVCAP service code.
"""
logger = None  # set when called by SDK

### TODO: Update the service args for Dbias
SERVICE = Service(
    name="toxicity-detection-automated",
    description="Basic automated approach to vulnerability discovery (toxic language generation) (Perez, Arxiv 2022).",
    parameters=[
        Parameter(
            name="model",
            type=Type.STRING,
            description="Model to use as RedLM.",
        ),
    ],
)


def service(args: ServiceArgs, svc_logger: logging):
    """Called after the service has started and all paramters have been parsed and validated

    Args:
        args (ServiceArgs): A Dict where the key is one of the `Parameter` defined in the above `SERVICE`
        svc_logger (logging): Logger to use for reporting information on the progress of execution
    """
    global logger
    logger = svc_logger

    """
    Automated vulnerability discovery based on technique introduced in:

    Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John
    Aslanides, Amelia Glaese, Nat McAleese, Geoffrey Irving (2022). Red Teaming
    Language Models with Language Models. arXiv:2202.03286
    """

    red_lm = HuggingFaceModel(name=args.model)
    result = _question_and_answers_zero_shot(
        red_lm=red_lm, num_samples=args.num_samples
    )
    result_json = _question_and_answers_few_shot(
        red_lm=red_lm, num_test_cases=args.num_samples, first_result=result
    )

    meta = create_metadata(
        "urn:guardrails:schema:toxicity-detection-automated", **args._asdict()
    )

    publish_artifact(
        "toxicity-detection-automated.json",
        lambda fd: json.dump(result_json, fd, indent=4),
        SupportedMimeTypes.JSON,
        metadata=meta,
    )


####
# Entry point
register_service(SERVICE, service)
