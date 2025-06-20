import threading
import collections.abc
from typing import TypeVar, Callable, Any, Dict, List, Union

# Sentinel object for default argument in `get` method to distinguish
# from `None` as a valid default value.
_SENTINEL = object()

T = TypeVar('T')

class Registry:
    """
    A thread-safe registry system for managing objects and factories.

    This registry allows for storing items (objects or callables that produce objects)
    under unique string names. It supports lazy initialization for items registered
    as factories, meaning the factory is only called when the item is first retrieved.
    Subsequent retrievals will return the cached instance.

    It is designed to be:
    - OOP Friendly: Manages objects and can be easily integrated into OOP designs.
    - Scalable: Uses efficient dictionary lookups and supports lazy loading.
    - Flexible: Allows registration of direct instances or factories, with an
                option to overwrite existing entries.
    - Thread-Safe: All public methods are protected by a lock to ensure safe
                   concurrent access.

    Note on factory execution and thread safety:
    Factory functions are executed synchronously while a lock is held on the registry.
    This ensures that the factory is resolved and the registry is updated atomically.
    Ensure factories are reasonably performant. If a factory performs long-running
    operations, consider designing it to manage such operations internally (e.g.,
    by returning a future or starting a background task and returning a proxy object)
    to avoid holding the registry lock for an extended period, which could become a
    contention point in highly concurrent scenarios.
    """
    def __init__(self):
        self._registry: Dict[str, Any] = {}
        self._is_factory: Dict[str, bool] = {}
        self._lock = threading.Lock()

    def register(self, name: str, item: T, overwrite: bool = False) -> None:
        """
        Registers an item directly.

        Args:
            name (str): The unique name to register the item under.
            item (T): The item to register.
            overwrite (bool, optional): If True, an existing item with the
                                        same name will be overwritten.
                                        Defaults to False.

        Raises:
            TypeError: If the name is not a string.
            ValueError: If an item with the same name already exists and
                        overwrite is False.
        """
        if not isinstance(name, str):
            raise TypeError("Registry key 'name' must be a string.")
        
        with self._lock:
            if name in self._registry and not overwrite:
                raise ValueError(
                    f"Item '{name}' already registered. "
                    "Set overwrite=True to replace."
                )
            self._registry[name] = item
            self._is_factory[name] = False

    def register_factory(self, name: str, factory: Callable[[], T], overwrite: bool = False) -> None:
        """
        Registers a factory function that will be called to create the item
        on its first retrieval. The result is then cached.

        Args:
            name (str): The unique name to register the factory under.
            factory (Callable[[], T]): A callable (function or method) that
                                         takes no arguments and returns the item.
            overwrite (bool, optional): If True, an existing item or factory
                                        with the same name will be overwritten.
                                        Defaults to False.

        Raises:
            TypeError: If the name is not a string or the factory is not callable.
            ValueError: If an item or factory with the same name already exists
                        and overwrite is False.
        """
        if not isinstance(name, str):
            raise TypeError("Registry key 'name' must be a string.")
        if not callable(factory):
            raise TypeError(f"Factory for '{name}' must be a callable.")

        with self._lock:
            if name in self._registry and not overwrite:
                raise ValueError(
                    f"Item or factory for '{name}' already registered. "
                    "Set overwrite=True to replace."
                )
            self._registry[name] = factory
            self._is_factory[name] = True

    def get(self, name: str, default: Any = _SENTINEL) -> Any:
        """
        Retrieves an item from the registry.

        If the registered item is a factory, it is called, and its result is
        cached for subsequent retrievals, replacing the factory in the registry.
        If the factory raises an exception during its execution, that exception
        will propagate to the caller of `get`, and the factory will remain
        registered as a factory (i.e., it will be attempted again on the next
        `get` call for that name).

        Args:
            name (str): The name of the item to retrieve.
            default (Any, optional): A default value to return if the item
                                     is not found. If not provided (i.e., remains
                                     _SENTINEL) and the item is not found,
                                     a KeyError is raised.

        Returns:
            Any: The retrieved item or the default value.

        Raises:
            KeyError: If the item is not found and no default value is provided.
            TypeError: If the name is not a string.
            Any other exception raised by a factory during its execution.
        """
        if not isinstance(name, str):
            raise TypeError("Registry key 'name' must be a string.")

        with self._lock:
            if name not in self._registry:
                if default is _SENTINEL:
                    raise KeyError(f"Item '{name}' not found in registry.")
                return default

            item_or_factory = self._registry[name]
            
            if self._is_factory[name]:
                # Item is a factory, resolve it.
                # The factory execution and update to the registry are atomic
                # due to the lock.
                try:
                    instance = item_or_factory()
                except Exception:
                    # If factory fails, let the exception propagate.
                    # The entry remains a factory and will be retried on next get().
                    raise
                
                self._registry[name] = instance
                self._is_factory[name] = False
                return instance
            else:
                # Item is already an instance
                return item_or_factory

    def unregister(self, name: str) -> bool:
        """
        Removes an item or factory from the registry.

        Args:
            name (str): The name of the item to unregister.

        Returns:
            bool: True if the item was found and removed, False otherwise.
        
        Raises:
            TypeError: If the name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Registry key 'name' must be a string.")
            
        with self._lock:
            if name in self._registry:
                del self._registry[name]
                del self._is_factory[name]
                return True
            return False

    def exists(self, name: str) -> bool:
        """
        Checks if an item or factory with the given name is registered.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if an item or factory with the name exists, False otherwise.

        Raises:
            TypeError: If the name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Registry key 'name' must be a string.")
            
        with self._lock:
            return name in self._registry

    def list_items(self) -> List[str]:
        """
        Returns a list of names of all registered items and factories.

        Returns:
            List[str]: A list of registered names.
        """
        with self._lock:
            return list(self._registry.keys())

    def clear(self) -> None:
        """
        Removes all items and factories from the registry.
        """
        with self._lock:
            self._registry.clear()
            self._is_factory.clear()