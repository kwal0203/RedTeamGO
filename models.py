from pydantic import BaseModel
from typing import List, Dict, Optional


class UserPrompt(BaseModel):
    prompt: str


class PromptLibrary(BaseModel):
    prompt_library_path: str


class Result(BaseModel):
    result: str
