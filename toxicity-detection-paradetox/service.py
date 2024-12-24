from src.services.toxicity_detection import detect_toxicity

from typing import Any


def service(args: Any) -> Any:
    # Toxicity detection service using the ParaDetox model (Logacheva, ACL 2022).

    # args.response: Generated response from an LLM

    ### Toxicity evaluation here
    result_json = detect_toxicity(response=args.response)
    return result_json
