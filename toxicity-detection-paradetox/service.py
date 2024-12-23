from ivcap_sdk_service import Service, Parameter, Type, SupportedMimeTypes, ServiceArgs
from ivcap_sdk_service import register_service, publish_artifact, create_metadata

from src.services.toxicity_detection import detect_toxicity

import logging
import json


"""
IVCAP service code.
"""
logger = None  # set when called by SDK

SERVICE = Service(
    name="toxicity-detection-paradetox",
    description="Toxicity detection service using the ParaDetox model (Logacheva, ACL 2022).",
    parameters=[
        Parameter(
            name="response",
            type=Type.STRING,
            description="Generated response from an LLM.",
        )
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

    ### Toxicity evaluation here
    result_json = detect_toxicity(response=args.response)
    meta = create_metadata(
        "urn:guardrails:schema:toxicity-detection-paradetox", **args._asdict()
    )

    publish_artifact(
        "toxicity-detection-paradetox.json",
        lambda fd: json.dump(result_json, fd, indent=4),
        SupportedMimeTypes.JSON,
        metadata=meta,
    )


####
# Entry point
register_service(SERVICE, service)
