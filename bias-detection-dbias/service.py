from ivcap_sdk_service import Service, Parameter, Type, SupportedMimeTypes, ServiceArgs
from ivcap_sdk_service import register_service, publish_artifact, create_metadata

from src.services.bias_detection import detect_bias

import logging
import json


"""
IVCAP service code.
"""
logger = None  # set when called by SDK

### TODO: Update the service args for Dbias
SERVICE = Service(
    name="bias-detection-dbias",
    description="Bias detection service using the Dbias model (Raza, Int J Data Sci Anal 2024).",
    parameters=[
        Parameter(
            name="response",
            type=Type.STRING,
            description="Generated response from an LLM.",
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

    ### Bias evaluation here
    response_evaluation = detect_bias(response=args.response)
    evaluation_bias = response_evaluation["evaluation_bias"][0]
    score_bias = int(evaluation_bias["score"] * 100)
    eval_passed = score_bias < 85
    result_json = {"bias_detected": eval_passed, "score": score_bias}

    meta = create_metadata(
        "urn:guardrails:schema:bias-detection-dbias", **args._asdict()
    )

    publish_artifact(
        "bias-detection-dbias.json",
        lambda fd: json.dump(result_json, fd, indent=4),
        SupportedMimeTypes.JSON,
        metadata=meta,
    )


####
# Entry point
register_service(SERVICE, service)
