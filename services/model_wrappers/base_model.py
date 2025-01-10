from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelMeta:
    name: Optional[str]
    description: Optional[str]


class ABC(metaclass=ABCMeta):
    """
    Helper class that provides a standard way to create an ABC using
    inheritance.
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
            description=description if description is not None else "default",
        )

    @property
    def name(self):
        if self.meta.name is not None:
            return self.meta.name
        else:
            return self.__class__.__name__

    @property
    def description(self):
        return self.meta.description


class WrapperModel(BaseModel, ABC):
    """
    A wrapper base class for all redteam models.

    Attributes:
        name (Optional[str]): The name of the wrapper model. Defaults to
            "my_model".
        description (Optional[str]): A description of the model being wrapped.
            Defaults to "Large language model".
    """

    def __init__(
        self,
        name: Optional[str] = "my_model",
        description: Optional[str] = "Large language model",
    ) -> None:
        """
        Initializes the WrapperModel with the given name and description.

        Args:
            name (Optional[str]): A name for the wrapper model. Defaults to
                "my_model".
            description (Optional[str]): A description of the model being
                wrapped. Defaults to "Large language model".
        """
        super().__init__(name=name, description=description)

    @abstractmethod
    def preprocess(self, data):
        """
        Abstract method for preprocessing input data.

        Args:
            data: The input data to be preprocessed.

        Returns:
            The preprocessed data.
        """
        pass

    @abstractmethod
    def postprocess(self, data):
        """
        Abstract method for postprocessing the model's output.

        Args:
            data: The output data from the model to be postprocessed.

        Returns:
            The postprocessed data.
        """
        pass

    @abstractmethod
    def model_predict(self, data):
        """
        Abstract method for generating predictions using the wrapped model.

        Args:
            data: The input data for the model.

        Returns:
            The model's predictions.
        """
        pass
