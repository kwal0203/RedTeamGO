from services.model_wrappers.base_model_remote import APIModel
from typing import Optional, List


class APIModelOpenai(APIModel):
    """
    A wrapper model class for interacting with the OpenAI API specifically.
    Inherits from APIModel and overrides _model_predict for OpenAI-specific behavior.
    """

    def __init__(
        self,
        name: Optional[str] = "openai_api_model",
        description: Optional[str] = "OpenAI model wrapper",
    ) -> None:
        """
        Initializes the OpenAI API model with the given name and description.
        """
        super().__init__(name=name, description=description)

    def _model_predict(self, inputs: List[str]) -> List[str]:
        """
        Sends preprocessed inputs to the OpenAI API and retrieves responses.

        Args:
            inputs (List[str]): A list of preprocessed input strings.

        Returns:
            List[str]: A list of responses from the OpenAI API.
        """
        responses = []
        for input_text in inputs:
            try:
                response = self.client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        # {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": input_text},
                    ],
                    max_tokens=150,
                    temperature=0.7,
                )
                responses.append(response["choices"][0]["message"]["content"])
            except Exception as e:
                responses.append(f"Error: {str(e)}")
        return responses
