from src.services.toxicity_detection import detect_toxicity
from models import DetectionBatch
from typing import Dict, Any


def paradetox_service(args: DetectionBatch) -> Dict[str, Any]:
    # Toxicity detection service using the ParaDetox model (Logacheva, ACL 2022).

    # args.response: Generated response from an LLM
    response = args.prompts

    ### Toxicity evaluation here
    return {"paradetox_result": detect_toxicity(response=response)}
