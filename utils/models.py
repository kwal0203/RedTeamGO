from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class UserPrompt(BaseModel):
    prompt: str


class PromptLibrary(BaseModel):
    prompt_library_path: str


class ResultBatch(BaseModel):
    result: Dict[str, Any]


class ResultRealtime(BaseModel):
    result: str


class Model(BaseModel):
    name: str
    description: str
    base_url: Optional[str]


class DetectionBatchToxicity(BaseModel):
    """
    For use in offline system auditing setting.
    """

    model: Model
    num_samples: int
    random: Optional[bool] = True
    database_prompts: Optional[bool] = True
    user_prompts: Optional[List[str]] = None
    user_topics: Optional[List[str]] = None


# class DetectionBatchBias(BaseModel):
#     """
#     For use in offline system auditing setting.
#     """

#     model: Model
#     prompts: Optional[PromptLibrary] = None
#     topics: Optional[List[str]] = [""]


class DetectionBatchBias(BaseModel):
    """
    For use in offline system auditing setting.
    """

    model: Model
    num_samples: int
    random: Optional[bool] = True
    database_prompts: Optional[bool] = True
    user_prompts: Optional[List[str]] = None
    user_topics: Optional[List[str]] = None


class ManualDetection(BaseModel):
    """
    For use in realtime setting (i.e. when chatting).
    """

    prompt: UserPrompt
