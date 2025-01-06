from pydantic import BaseModel
from typing import List, Dict, Optional


class UserPrompt(BaseModel):
    prompt: str


class PromptLibrary(BaseModel):
    prompt_library_path: str


class ResultBatch(BaseModel):
    result: Dict


class ResultRealtime(BaseModel):
    result: str


class Model(BaseModel):
    model: str


class DetectionBatch(BaseModel):
    """
    For use in offline system auditing setting.
    """

    prompts: Optional[PromptLibrary]
    model: Model

    # The automated toxicity detector needs num_samples
    # ParaDetox requires a response from an LLM to analyze


class ManualDetection(BaseModel):
    """
    For use in realtime setting (i.e. when chatting).
    """

    prompt: UserPrompt
