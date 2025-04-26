import loguru
from aiohttp import web
from typing import Callable
    

class HttpRouter:
    def __init__(self):
        self._routes = web.RouteTableDef()

    def route(self, method: str, path: str, handler: Callable):
        """Decorator to add a route."""
        return self._routes.route(method, path)(handler)

    def get(self, path: str, handler: Callable):
        """Decorator for GET requests."""
        return self.route("GET", path, handler)

    def post(self, path: str, handler: Callable):
        """Decorator for POST requests."""
        return self.route("POST", path, handler)

    def put(self, path: str, handler: Callable):
        """Decorator for PUT requests."""
        return self.route("PUT", path, handler)

    def delete(self, path: str, handler: Callable):
        """Decorator for DELETE requests."""
        return self.route("DELETE", path, handler)

    def add_routes(self, app: web.Application):
        """Add all registered routes to the application."""
        app.add_routes(self._routes)

    def register_routes_from_module(self, module):
        """Register routes defined in a module."""
        for name, obj in module.__dict__.items():
            if callable(obj) and hasattr(obj, '__routes__'):
                for route in obj.__routes__:
                    method, path, handler_name = route  # You're storing the handler *name*
                    handler = getattr(module, handler_name) # Get the actual function
                    self.route(method, path, handler)
                loguru.logger.debug(f"Registered routes from function/method: {module.__name__}.{name}")

    def register_routes_from_class(self, cls):
        """Register routes defined as methods within a class."""
        for name in dir(cls):
            method = getattr(cls, name)
            if callable(method) and hasattr(method, '__routes__'):
                instance = cls()  # Instantiate the class to access methods
                for route in method.__routes__:
                    http_method, path, handler_name = route
                    handler = getattr(instance, handler_name)
                    self.route(http_method, path, handler)
                loguru.logger.debug(f"Registered routes from class: {cls.__name__}")

# Create a global router instance
router = HttpRouter()


# Custom decorator to mark route handlers
def route(method: str, path: str):
    def decorator(func):
        if not hasattr(func, '__routes__'):
            func.__routes__ = []
        func.__routes__.append((method, path, func.__name__)) # Store handler name for class-based routes
        return func
    return decorator

# Convenience decorators for HTTP methods
def get(path: str):
    return route("GET", path)

def post(path: str):
    return route("POST", path)

def put(path: str):
    return route("PUT", path)

def delete(path: str):
    return route("DELETE", path)

