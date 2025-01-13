from services.model_wrappers.base_model_remote import APIModel
from typing import List, Optional

import openai


class APIModelGPTModerator(APIModel):
    """
    A wrapper model class for interacting with the OpenAI Moderator API.
    Inherits from APIModel and overrides _model_predict for Moderator-specific behavior.
    """

    def __init__(
        self,
        name: Optional[str] = "openai_moderator_api_model",
        description: Optional[str] = "OpenAI Moderator model wrapper",
    ) -> None:
        """
        Initializes the OpenAI Moderator API model with the given name and description.
        """
        super().__init__(name=name, description=description)

    def _model_predict(self, inputs: List[str]) -> List[str]:
        """
        Sends inputs to the OpenAI Moderator API and retrieves moderation results.

        Args:
            inputs (List[str]): A list of preprocessed input strings.

        Returns:
            List[str]: A list of moderation results (safe/unsafe labels) for each input.
        """
        results = []
        for input_text in inputs:
            try:
                response = openai.moderations.create(input=input_text).to_dict()
                moderation_result = response["results"][0]["category_scores"]
                results.append(moderation_result)
            except Exception as e:
                results.append(f"Error: {str(e)}")
        return results
