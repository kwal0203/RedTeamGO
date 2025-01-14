from services.model_wrappers.base_model import WrapperModel
from typing import Optional, List
from transformers import (
    RobertaTokenizer,
    RobertaForSequenceClassification,
)
from utils.config import get_device

import numpy as np


class ParadetoxModerator(WrapperModel):
    """
    This class provides a wrapper for the model from:

    Varvara Logacheva, Daryna Dementieva, Sergey Ustyantsev, Daniil Moskovskiy,
    David Dale, Irina Krotova, Nikita Semenov, and Alexander Panchenko. 2022.
    ParaDetox: Detoxification with Parallel Data. In Proceedings of the 60th
    Annual Meeting of the Association for Computational Linguistics.
    Association for Computational Linguistics.

    Attributes:
        name (Optional[str]): TODO.
        decription (Optional[str]): TODO.
        model (Any): TODO.
        tokenizer (Any): TODO.

    Methods:
        preprocess: TODO.
        postprocess: TODO.
        model_predict: TODO.
        _model_predict: TODO.
    """

    def __init__(
        self,
        name: Optional[str] = "my_paradetox_model",
        description: Optional[str] = "Local large language model",
    ) -> None:
        """
        Initializes the ParaDetox wrapper class.

        Args:
            path (str): Path to the local model directory or HuggingFace model ID.
            name Optional[str]: Name of the model being wrapped.
            description Optional[str]: Description of the model being wrapped.
        """
        super().__init__(name=name, description=description)

        # Load the model and tokenizer
        path = "s-nlp/roberta_toxicity_classifier"
        self.model = RobertaForSequenceClassification.from_pretrained(path)
        self.tokenizer = RobertaTokenizer.from_pretrained(path)
        self.device = get_device()
        self.model.to(self.device)

    def preprocess(self, data: List[str]) -> List[str]:
        """
        Preprocess prompt.

        Args:
            data (List[str]): TODO.
        """
        return self.tokenizer.encode(data, return_tensors="pt")

    def postprocess(self, generated_text):
        """
        Postprocess text generated by LLM.

        Args:
            generated_text (List[str]): TODO.
        """
        return generated_text

    def model_predict(self, data: List[str]) -> List[str]:
        """
        Obtain generated responses after inputting prompts. Perform input and
        output processing if required.

        Args:
            data (List[str]): TODO.
        """

        input = self.preprocess(data=data[0])
        response = self._model_predict(inputs=input)
        output = self.postprocess(generated_text=response)
        return output

    def _model_predict(self, inputs) -> List[str]:
        """
        Helper function for obtaining generated response from input prompts.

        Args:
            inputs (List[int]): TODO.
        """
        response_evaluation = self.model(inputs)

        def softmax(logits):
            exp_logits = np.exp(logits)
            return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

        # Use tensor.detach().numpy() instead.
        toxicity_probability = softmax(
            [
                response_evaluation.logits[0][0].detach().numpy(),
                response_evaluation.logits[0][1].detach().numpy(),
            ]
        )

        return toxicity_probability[1]
