import importlib
import inspect
import logging
import os
from typing import Dict, List, Type

from .base_redteam_method import BaseRedTeamMethod, RedTeamMethodMetadata

logger = logging.getLogger(__name__)


class RedTeamMethodRegistry:
    """Registry for managing red teaming methods.

    This class handles dynamic loading and management of red teaming methods,
    making it easy to add new methods without modifying existing code.
    """

    def __init__(self):
        self._methods: Dict[str, BaseRedTeamMethod] = {}
        self._method_classes: Dict[str, Type[BaseRedTeamMethod]] = {}

    async def initialize(self) -> None:
        """Initialize the registry by discovering and loading all available methods."""
        await self._discover_methods()

    async def _discover_methods(self) -> None:
        """Discover all red teaming methods in the services directory."""
        services_dir = os.path.dirname(os.path.abspath(__file__))

        # Scan all directories in services
        for item in os.listdir(services_dir):
            if not os.path.isdir(os.path.join(services_dir, item)):
                continue

            if item.startswith("__") or item == "model_wrappers":
                continue

            try:
                # Import the module
                module_path = f"services.{item}"
                module = importlib.import_module(module_path)

                # Find all classes that inherit from BaseRedTeamMethod
                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseRedTeamMethod)
                        and obj != BaseRedTeamMethod
                    ):

                        method_id = f"{item}.{name}"
                        self._method_classes[method_id] = obj
                        logger.info(f"Discovered red teaming method: {method_id}")

            except Exception as e:
                logger.error(f"Error loading method from {item}: {str(e)}")

    async def load_method(self, method_id: str) -> None:
        """Load and initialize a specific method."""
        if method_id not in self._method_classes:
            raise ValueError(f"Unknown method: {method_id}")

        if method_id in self._methods:
            return  # Already loaded

        try:
            method = self._method_classes[method_id]()
            await method.initialize()
            self._methods[method_id] = method
            logger.info(f"Loaded method: {method_id}")
        except Exception as e:
            logger.error(f"Error initializing method {method_id}: {str(e)}")
            raise

    async def unload_method(self, method_id: str) -> None:
        """Unload a specific method."""
        if method_id in self._methods:
            try:
                await self._methods[method_id].cleanup()
                del self._methods[method_id]
                logger.info(f"Unloaded method: {method_id}")
            except Exception as e:
                logger.error(f"Error cleaning up method {method_id}: {str(e)}")
                raise

    def get_method(self, method_id: str) -> BaseRedTeamMethod:
        """Get a loaded method instance."""
        if method_id not in self._methods:
            raise ValueError(f"Method not loaded: {method_id}")
        return self._methods[method_id]

    def list_available_methods(self) -> List[str]:
        """List all available method IDs."""
        return list(self._method_classes.keys())

    def list_loaded_methods(self) -> List[str]:
        """List currently loaded method IDs."""
        return list(self._methods.keys())

    def get_method_metadata(self, method_id: str) -> RedTeamMethodMetadata:
        """Get metadata for a specific method."""
        if method_id in self._methods:
            return self._methods[method_id].get_metadata()
        elif method_id in self._method_classes:
            method = self._method_classes[method_id]()
            return method.get_metadata()
        else:
            raise ValueError(f"Unknown method: {method_id}")

    async def cleanup(self) -> None:
        """Clean up all loaded methods."""
        for method_id in list(self._methods.keys()):
            await self.unload_method(method_id)
