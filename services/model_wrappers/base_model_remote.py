from services.model_wrappers.base_model import WrapperModel
from typing import Optional, Dict, List
from utils.config import get_openai_key

import openai


class APIModel(WrapperModel):
    """
    A wrapper model class for interacting with a remote large language model via API.

    Attributes:
        name (Optional[str]): The name of the API model. Defaults to "my_api_model".
        description (Optional[str]): A description of the model being wrapped. Defaults to "Remote large language model".
        openai_key (str): The API key used for authentication with the OpenAI endpoint.
    """

    def __init__(
        self,
        name: Optional[str] = "my_api_model",
        description: Optional[str] = "Remote large language model",
    ) -> None:
        """
        Initializes the APIModel with the given name and description, and sets up the OpenAI API key.

        Args:
            name (Optional[str]): The name of the API model. Defaults to "my_api_model".
            description (Optional[str]): A description of the model being wrapped. Defaults to "Remote large language model".
        """
        super().__init__(name=name, description=description)
        openai.api_key = get_openai_key()
        self.client = openai

    def preprocess(self, data: List[Dict]) -> List[str]:
        """
        Preprocesses input data before sending it to the model.

        Args:
            data (List[Dict]): A list of dictionaries representing the input data.

        Returns:
            List[str]: A list of preprocessed strings.
        """
        return data

    def postprocess(self, response):
        """
        Postprocesses the model's response to prepare it for output.

        Args:
            response: The raw response from the model.

        Returns:
            The processed response.
        """
        return response

    def model_predict(self, data: List[str]) -> List[str]:
        """
        Generates predictions from the model for the given input data.

        Args:
            data (List[str]): A list of strings representing the input data.

        Returns:
            List[str]: A list of model predictions.
        """
        input = self.preprocess(data=data)
        response = self._model_predict(inputs=input)
        output = self.postprocess(response=response)
        return output

    def _model_predict(self, inputs: List[str]) -> List[str]:
        """
        Sends preprocessed inputs to the remote model and retrieves responses.

        Args:
            inputs (List[str]): A list of preprocessed input strings.

        Returns:
            List[str]: A list of responses from the remote model.
        """
        # TODO: set this up so it queries the provided FastAPI endpoint
        responses = []
        for input in inputs:
            responses.append(self.model(input))
        return responses
