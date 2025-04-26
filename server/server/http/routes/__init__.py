from server.http.Router import HttpRouter, router
from server.http.routes.LoginApi import login_handler
from server.http.routes.SignupApi import signup_handler
from server.http.routes.StatusApi import status_handler
from utils.AppServices import AppServices


def register_routes(http_router: HttpRouter, services: AppServices):
    """
    This function is no longer strictly necessary with the global router.
    However, you can keep it for potential modularity or if you prefer
    explicit registration within the module.
    """
    router.post("/login", lambda request: login_handler(request, services))
    router.post("/signup", lambda request: signup_handler(request, services))

    router.get("/", lambda request: status_handler(request, services))