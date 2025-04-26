# server/http/http_server.py
import asyncio
import loguru
from aiohttp import web

from utils.AppServices import AppServices
from .Router import router  # Import Router class and instance
import server.http.routes.LoginApi  # Import your route modules



class HttpServer:
    def __init__(self, host: str, port: int, services: AppServices):
        self.host = host
        self.port = port
        self.services = services
        self.app = web.Application()
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