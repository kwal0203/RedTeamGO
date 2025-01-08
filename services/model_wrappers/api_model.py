from services.model_wrappers.base_model import WrapperModel
from typing import Optional, Dict, List


class APIModel(WrapperModel):
    """
    This class provides a wrapper for models that are queried through an API.

    Attributes:
        name (str): TODO.
        batch_size (int): TODO.
        prompts (Dict): TODO.

    Methods:
        preprocess: TODO.
        model_predict: TODO.
        _model_predict: TODO.
        postprocess: TODO.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        batch_size: Optional[int] = 1,
        prompts: Dict = None,
    ) -> None:
        """
        Initializes the ToxicityEvaluationModel class.

        Args:
            name (str): The name of the model.
            batch_size (int): The batch size used for inference. Default to 1.
            prompts (Dict): A dictionary required prompts including system
                and/or user prompts.
        """
        super().__init__(
            model=name,
            name=name,
        )

        self.batch_size = batch_size
        self.prompts = prompts

    def preprocess(self, data: List[Dict]) -> List[str]:
        """
        Preprocesses input prompts

        Args:
            data (List[Dict]): TODO.
        """
        return data

    def model_predict(self, data: List[str]) -> List[str]:
        """
        Obtain generated responses after inputting prompts.

        Args:
            data (List[str]): TODO.
        """
        inputs = self.preprocess(data=data)
        return self._model_predict(inputs=inputs)

    def _model_predict(self, inputs) -> List[str]:
        """
        Helper function for obtaining generated response from input prompts.

        Args:
            inputs (List[int]): TODO.
        """
        responses = []
        for input in inputs:
            responses.append(self.model(input))
        return responses

    def postprocess(self, responses):
        """
        Postprocessing of generated responses.

        Args:
            responses (List[str]): TODO.
        """
        return responses
