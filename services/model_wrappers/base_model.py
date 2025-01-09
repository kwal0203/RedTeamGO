from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Optional


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
            name (Optional[str]): Name of the model. If not provided, defaults
                to the class name.
            description (Optional[str]): Description of the model's task.
                Mandatory for non-langchain text_generation models.

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
        name (Optional[str]): TODO.
        decription (Optional[str]): TODO.

    Methods:
        preprocess: TODO.
        postprocess: TODO.
        model_predict: TODO.
    """

    def __init__(
        self,
        name: Optional[str] = "my_model",
        description: Optional[str] = "Large language model",
    ) -> None:
        """
        Initializes WrapperModel with following attributes.

        Args:
            name Optional[str]: A name for the wrapper class.
            description Optional[str]: Description of the model being wrapped.
        """
        super().__init__(name=name, description=description)

    @abstractmethod
    def preprocess(self, data): ...

    @abstractmethod
    def postprocess(self, data): ...

    @abstractmethod
    def model_predict(self, data): ...
