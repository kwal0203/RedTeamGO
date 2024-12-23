from ivcap_sdk_service import Service, Parameter, Type, SupportedMimeTypes, ServiceArgs
from ivcap_sdk_service import register_service, publish_artifact, create_metadata

from src.utility.atomic_facts import get_atomic_facts
from src.services.hallucination_detection import detect

import logging
import json
import nltk


"""
IVCAP service code.
"""
logger = None  # set when called by SDK

SERVICE = Service(
    name="hallucination-detection-factscore",
    description="Proof of concept hallucination detection system using FActScore method for document summarization.",
    parameters=[
        Parameter(
            name="summary",
            type=Type.STRING,
            description="Document summary.",
        ),
        Parameter(
            name="source",
            type=Type.STRING,
            description="Ground truth.",
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

    ### FActScore
    # Summary
    # LLM-based approach to hallucination detection
    # Fact score from:
    # FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long
    # Form Text Generation (Min, 2023)
    generated_summary = args.summary

    # Split generation into sentences
    sentences = nltk.tokenize.sent_tokenize(generated_summary)

    # Get atomic facts
    # Note: they have alot of weird conditions like checking for sentences that start with "Sure"
    # Note: For each sentence want to see if that sentence makes a factual claim about genomics
    # Note: One issue is that some sentences are not atomic true/false statements
    #       - hallucination is different to off-topic i.e. when inserting comments about swimmingS
    atomic_facts = get_atomic_facts(sentences=sentences)
    result_json = detect(source=args.source, atomic_facts=atomic_facts)
    result_json["summary"] = generated_summary

    meta = create_metadata(
        "urn:guardrails:schema:hallucination-detection-factscore", **args._asdict()
    )

    publish_artifact(
        "factscore.json",
        lambda fd: json.dump(result_json, fd, indent=4),
        SupportedMimeTypes.JSON,
        metadata=meta,
    )


####
# Entry point
register_service(SERVICE, service)
