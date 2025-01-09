from services.model_wrappers.base_model import WrapperModel
from typing import Optional, Dict, List
from utils.config import api_key_openai


class APIModel(WrapperModel):
    """
    This class provides a wrapper for models that are queried through an API.

    Attributes:
        name (Optional[str]): TODO.
        decription (Optional[str]): TODO.
        openai_key (str): TODO.

    Methods:
        preprocess: TODO.
        model_predict: TODO.
        _model_predict: TODO.
        postprocess: TODO.
    """

    def __init__(
        self,
        name: Optional[str] = "my_api_model",
        description: Optional[str] = "Large language model",
    ) -> None:
        """
        Initializes the ToxicityEvaluationModel class.

        Args:
            name (str): The name of the model.
            batch_size (int): The batch size used for inference. Default to 1.
            prompts (Dict): A dictionary required prompts including system
                and/or user prompts.
        """
        super().__init__(name=name, description=description)
        self.openai_key = api_key_openai

    def preprocess(self, data: List[Dict]) -> List[str]:
        """
        Preprocesses input prompts

        Args:
            data (List[Dict]): TODO.
        """
        return data

    def postprocess(self, response):
        """
        Postprocessing of generated responses.

        Args:
            response (List[str]): TODO.
        """
        return response

    def model_predict(self, data: List[str]) -> List[str]:
        """
        Obtain generated responses after inputting prompts. Perform input and
        output processing if required.

        Args:
            data (List[str]): TODO.
        """
        input = self.preprocess(data=data)
        response = self._model_predict(inputs=input)
        output = self.postprocess(responses=response)
        return output

    def _model_predict(self, inputs) -> List[str]:
        """
        Helper function for obtaining generated response from input prompts.

        Args:
            inputs (List[int]): TODO.
        """
        # TODO: set this up so it queries the provided FastAPI endpoint
        responses = []
        for input in inputs:
            responses.append(self.model(input))
        return responses
