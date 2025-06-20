
from typing import Callable, Type, TypeVar, Dict, List
from enum import Enum
from weakref import WeakSet

import loguru


class Cancellable(object):
    def cancel():
        raise Exception("NotImplementedException")

class Event:
    def __init__(self):
        pass

    def is_cancelled(self) -> bool:
        return False

    def cancel(self):
        raise Exception("Event is not cancellable.")

    def call(self) -> bool:
        EventHandler.dispatch_event(self)
        return not self.is_cancelled()

class HandlerPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3


# Type hint for event listeners
T = TypeVar('T', bound=Event)
EventListener = Callable[[T], None]

class EventHandler:
    _listeners: Dict[Type[Event], List[tuple[HandlerPriority, EventListener, WeakSet[object], bool]]] = {}

    @staticmethod
    def register_listener(
        plugin: object,  # Could be any object representing the registrant
        event_class: Type[T],
        listener: EventListener[T],
        priority: HandlerPriority = HandlerPriority.NORMAL,
        handle_cancelled: bool = False,
    ):
        if event_class not in EventHandler._listeners:
            EventHandler._listeners[event_class] = []
        # Store the listener along with its priority, the registering plugin (weakly referenced), and the handle_cancelled flag
        EventHandler._listeners[event_class].append((priority, listener, WeakSet([plugin]), handle_cancelled))
        # Keep the listeners sorted by priority (higher priority first)
        EventHandler._listeners[event_class].sort(key=lambda item: item[0].value, reverse=True)

    @staticmethod
    def unregister_listener(plugin: object, event_class: Type[T], listener: EventListener[T]):
        if event_class in EventHandler._listeners:
            EventHandler._listeners[event_class] = [
                item for item in EventHandler._listeners[event_class]
                if item[1] != listener or plugin not in item[2]
            ]
            if not EventHandler._listeners[event_class]:
                del EventHandler._listeners[event_class]

    @staticmethod
    def unregister_plugin_listeners(plugin: object):
        for event_class in list(EventHandler._listeners.keys()):
            EventHandler._listeners[event_class] = [
                item for item in EventHandler._listeners[event_class] if plugin not in item[2]
            ]
            if not EventHandler._listeners[event_class]:
                del EventHandler._listeners[event_class]

    @staticmethod
    def dispatch_event(event: T):
        event_class = type(event)
        if event_class in EventHandler._listeners:
            for priority, listener, plugins, handle_cancelled in EventHandler._listeners[event_class]:
                if not event.is_cancelled() or handle_cancelled:
                    try:
                        listener(event)
                    except Exception as e:
                        loguru.logger.error(f"Error during event handling for {event_class.__name__}: {e}")