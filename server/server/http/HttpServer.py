# server/http/http_server.py
import asyncio
import time
from typing import Awaitable, Callable
import loguru
from aiohttp import web

from utils.AppServices import AppServices
from .Router import router  # Import Router class and instance
import server.http.routes


async def logging_middleware(request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]) -> web.Response:
    """
    Middleware to log incoming requests and their processing time.
    """
    start_time = asyncio.get_event_loop().time()
    loguru.logger.info(f"Incoming request: {request.method} {request.path}")
    try:
        response = await handler(request)
    except Exception as e:
        #  Log the error
        loguru.logger.error(f"Error handling {request.method} {request.path}: {e}")
        #  Re-raise the error so aiohttp can handle it (important!)
        raise
    finally:  # Use a finally block to ensure this always runs
        end_time = asyncio.get_event_loop().time()
        loguru.logger.info(f"Request handled in {end_time - start_time:.3f} seconds: {request.method} {request.path} -> {response.status}")
    return response

async def timestamp_middleware(request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]) -> web.Response:
    """
    Middleware to timestamp every response
    """
    response = await handler(request)  # Get the response from the handler
    response.headers['X-Server-Timestamp'] = time.time()  # Add the header
    return response


class HttpServer:
    def __init__(self, host: str, port: int, services: AppServices):
        self.host = host
        self.port = port
        self.services = services
        self.app = web.Application(middlewares=[timestamp_middleware, logging_middleware])
        self.router = router  # Use the globally available router instance
        self._setup_routes()
        self.runner = None
        self.site = None


    def _setup_routes(self):
        """Register all the routes for the HTTP server."""
        server.http.routes.register_routes(self.router, self.services)
        # Import and register other route modules here
        # import server.http.routes.AdminApi
        # server.http.routes.AdminApi.register_routes(self.router)
        self.router.add_routes(self.app)

    async def start(self):
        """Start the HTTP server."""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        loguru.logger.info(f"HTTP server started on http://{self.host}:{self.port}")
        return self.runner

    async def stop(self):
        """Stop the HTTP server."""
        if self.runner:
            await self.runner.cleanup()
        loguru.logger.info("HTTP server stopped.")