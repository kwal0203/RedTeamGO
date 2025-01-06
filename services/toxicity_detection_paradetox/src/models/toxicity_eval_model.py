from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from transformers import (
    RobertaTokenizer,
    RobertaForSequenceClassification,
)


@dataclass
class ModelMeta:
    name: Optional[str]
    description: Optional[str]


class ABC(metaclass=ABCMeta):
    """
    Helper class that provides a standard way to create an ABC using inheritance.
    """

    __slots__ = ()


class BaseModel(ABC):
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Initialize a new instance of the BaseModel class.

        Parameters:
            name (Optional[str]): Name of the model. If not provided, defaults to the class name.
            description (Optional[str]): Description of the model's task. Mandatory for non-langchain text_generation models.

        Raises:
            ValueError: If an invalid model_type value is provided.
        """

        self.meta = ModelMeta(
            name=name if name is not None else self.__class__.__name__,
            description=description if description is not None else "No description",
        )

    @property
    def name(self):
        return self.meta.name if self.meta.name is not None else self.__class__.__name__

    @property
    def description(self):
        return self.meta.description


class WrapperModel(BaseModel, ABC):
    """
    Wrapper base class for all redteam models.

    Attributes:
        model (Any): TODO.
        tokenizer (Any): TODO.
        batch_size (int): TODO.

    Methods:
        preprocess: TODO.
        model_predict: TODO.
        postprocess: TODO.
    """

    def __init__(
        self,
        model: Any,
        tokenizer: Optional[Any] = None,
        name: Optional[str] = None,
        batch_size: Optional[int] = None,
    ) -> None:
        """
        Initializes WrapperModel with following attributes.

        Args:
            model (Any): The model that will be wrapped.
            name Optional[str]: A name for the wrapper. Default is ``None``.
            batch_size Optional[int]: The batch size to use for inference. Default is ``None``, which means inference will be done on the full input data.
        """
        super().__init__(
            name=name,
        )
        self.model = model
        self.tokenizer = tokenizer
        self.batch_size = batch_size

    @abstractmethod
    def preprocess(self, data): ...

    @abstractmethod
    def model_predict(self, data): ...

    @abstractmethod
    def postprocess(self, data): ...


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
