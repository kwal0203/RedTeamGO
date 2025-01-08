from services.model_wrappers.base_model import WrapperModel
from typing import Optional, Dict, List
from transformers import (
    RobertaTokenizer,
    RobertaForSequenceClassification,
)


class ToxicityEvaluationModel(WrapperModel):
    """
    This class provides a wrapper for HuggingFace models from the 'transformers'
    library for use as redteam evaluation models.

    Attributes:
        model (Any): TODO.
        tokenizer (Any): TODO.
        name (str): TODO.
        huggingface_module (str): TODO.
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
            model (Any): The model instance to be wrapped. Should be an
            instance of a HuggingFace model (i.e. from the ``transformers``
            library).
            tokenizer (Any): The tokenizer for the given HuggingFace model.
            name (str): The name of the model.
            batch_size (int): The batch size used for inference. Default to 1.
            prompts (Dict): A dictionary containing system and user prompts.
        """
        super().__init__(
            model=RobertaForSequenceClassification.from_pretrained(name),
            tokenizer=RobertaTokenizer.from_pretrained(name),
            name=name,
        )

        self.huggingface_module = self.model.__class__
        self.batch_size = batch_size
        self.prompts = prompts
        # self.model.to(device)

    def preprocess(self, data: List[Dict]) -> List[str]:
        """
        Preprocesses input prompts

        Args:
            data (List[Dict]): TODO.
        """
        return self.tokenizer.encode(data, return_tensors="pt")

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
        return self.model(inputs)

    def postprocess(self, responses):
        """
        Postprocessing of generated responses.

        Args:
            responses (List[str]): TODO.
        """
        return responses
