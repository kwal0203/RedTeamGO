from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class RedTeamMethodMetadata(BaseModel):
    """Metadata for a red teaming method."""

    name: str
    version: str
    description: str
    tags: List[str]
    requires_gpu: bool = False
    average_latency_ms: Optional[float] = None


class RedTeamMethodResult(BaseModel):
    """Standard result format for red teaming methods."""

    score: float
    confidence: float
    details: Dict[str, Any]
    warnings: List[str] = []
    metadata: Dict[str, Any] = {}


class BaseRedTeamMethod(ABC):
    """Abstract base class for all red teaming methods.

    All new red teaming methods should inherit from this class and implement
    the required methods. This ensures consistency across different implementations
    and makes it easier to add new methods.
    """

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the method, loading any required models or resources."""
        pass

    @abstractmethod
    def get_metadata(self) -> RedTeamMethodMetadata:
        """Return metadata about this red teaming method."""
        pass

    @abstractmethod
    async def evaluate(
        self, prompt: str, response: str, context: Optional[Dict[str, Any]] = None
    ) -> RedTeamMethodResult:
        """Evaluate a prompt-response pair using this red teaming method.

        Args:
            prompt: The input prompt
            response: The model's response
            context: Optional additional context (e.g., conversation history)

        Returns:
            RedTeamMethodResult containing the evaluation results
        """
        pass

    @abstractmethod
    async def batch_evaluate(
        self,
        prompts: List[str],
        responses: List[str],
        contexts: Optional[List[Dict[str, Any]]] = None,
    ) -> List[RedTeamMethodResult]:
        """Evaluate multiple prompt-response pairs in batch.

        Default implementation calls evaluate() for each pair, but methods
        can override this for more efficient batch processing.
        """
        results = []
        for i, (prompt, response) in enumerate(zip(prompts, responses)):
            context = contexts[i] if contexts else None
            result = await self.evaluate(prompt, response, context)
            results.append(result)
        return results

    async def cleanup(self) -> None:
        """Clean up any resources. Called when the method is being unloaded."""
        pass

    def get_requirements(self) -> Dict[str, str]:
        """Return a dictionary of package requirements for this method."""
        return {}
