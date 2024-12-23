from ivcap_sdk_service import Service, Parameter, Type, SupportedMimeTypes, ServiceArgs
from ivcap_sdk_service import register_service, publish_artifact, create_metadata


import logging
import json
import math


"""
IVCAP service code.
"""
logger = None  # set when called by SDK

SERVICE = Service(
    name="hallucination-detection-model-confidence",
    description="Proof of concept hallucination detection system using model confidence method for document summarization.",
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
    global logger
    logger = svc_logger

    # Token level model confidence approach to hallucination
    # Seq-logprobs from:
    # Looking for a Needle in a Haystack: A Comprehensive Study of
    # Hallucinations in Neural Machine Translation (Guerreiro, 2023)
    ### Model confidence
    logprobs = args.logprobs
    avg_logprobs = sum([log_prob["logprob"] for log_prob in logprobs]) / len(logprobs)
    seq_logprob = int(math.exp(avg_logprobs) * 100)
    result_json = {"model_confidence": seq_logprob}

    meta = create_metadata(
        "urn:guardrails:schema:hallucination-detection-model-confidence",
        **args._asdict()
    )

    publish_artifact(
        "model_confidence.json",
        lambda fd: json.dump(result_json, fd, indent=4),
        SupportedMimeTypes.JSON,
        metadata=meta,
    )


####
# Entry point
register_service(SERVICE, service)
