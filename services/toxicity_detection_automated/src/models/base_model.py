from typing import Optional, Any
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod


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
