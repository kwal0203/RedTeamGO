from services.models.base_model import WrapperModel
from typing import Optional, Dict, List
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)
from env import device

import os
import logging
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("tensorflow").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")


class HuggingFaceModel(WrapperModel):
    """
    This class provides a wrapper for HuggingFace models from the 'transformers' library.

    Attributes:
        model (Any): TODO.
        tokenizer (Any): TODO.
        name (str): TODO.
        huggingface_module (str): TODO.
        batch_size (int): TODO.
        prompts (Dict): TODO.


    Methods:
        preprocess: TODO.
        _format_inputs_huggingface: TODO.
        model_predict: TODO.
        _model_predict: TODO.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        batch_size: Optional[int] = 1,
        prompts: Dict = None,
    ) -> None:
        """
        Initializes the HuggingFaceModel class.

        Args:
            model (Any): The model instance to be wrapped. Should be an instance of a HuggingFace model (i.e. from the ``transformers`` library).
            tokenizer (Any): The tokenizer for the given HuggingFace model.
            name (str): The name of the model.
            batch_size (int): The batch size used for inference. Default to 1.
            prompts (Dict): A dictionary containing system and user prompts.
        """
        super().__init__(
            model=AutoModelForCausalLM.from_pretrained(name),
            tokenizer=AutoTokenizer.from_pretrained(name),
            name=name,
        )

        self.huggingface_module = self.model.__class__
        self.batch_size = batch_size
        self.prompts = prompts
        self.model.to(device)

    def preprocess(self, data: List[Dict]) -> List[str]:
        """
        Preprocesses input prompts

        Args:
            data (List[Dict]): TODO.
        """
        inputs = []
        for prompt in data:
            messages = self._format_inputs_huggingface(question=prompt)
            inputs.append(messages)

        return inputs

    def _format_inputs_huggingface(
        self,
        question: str,
    ) -> str:
        """
        Helper function for preprocessing input prompts.

        Args:
            question (str): TODO.
        """
        result = f"{question}:"
        return result

    def model_predict(self, data: List[str]) -> List[str]:
        """
        Obtain generated responses after inputting prompts.

        Args:
            data (List[str]): TODO.
        """
        inputs = self.preprocess(data)
        inputs_processed = [
            self.tokenizer(i + self.tokenizer.eos_token, return_tensors="pt").to(device)
            for i in inputs
        ]
        return self._model_predict(self.tokenizer, self.model, inputs_processed)

    def _model_predict(self, tokenizer, model, inputs) -> List[str]:
        """
        Helper function for obtaining generated response from input prompts.

        Args:
            tokenizer (Any): TODO.
            model (Any): TODO.
            inputs (List[int]): TODO.
        """
        responses = []
        for input in inputs:
            outputs = model.generate(
                input.input_ids,
                max_length=500,
                pad_token_id=tokenizer.eos_token_id,
                num_return_sequences=1,
            )
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
            responses.append(generated_text)
        return responses

    def postprocess(self, responses):
        """
        Postprocessing of generated responses. Note, this postprocessing code will change
        depecing on model/system prompt used and its specific output format.

        Args:
            responses (List[str]): TODO.
        """
        return [response.split("end_header_id|>")[1] for response in responses]
