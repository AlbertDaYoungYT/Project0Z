from server.http.Router import HttpRouter, router
from server.http.routes.LoginApi import login_handler
from server.http.routes.SignupApi import signup_handler
from server.http.routes.StatusApi import status_handler
from server.http.routes.log.CrashReporter import crash_report_handler
from server.http.routes.auth.InitHello import initial_greeting_handler
from server.http.routes.auth.InitAck import initial_ack_handler
from server.http.routes.auth.SigningChallengeRequest import signing_challenge_handler
from server.http.routes.auth.SigningChallengeSubmit import challenge_submission_handler
from utils.AppServices import AppServices


def register_routes(http_router: HttpRouter, services: AppServices):
    """
    This function is no longer strictly necessary with the global router.
    However, you can keep it for potential modularity or if you prefer
    explicit registration within the module.
    """
    router.get("/", status_handler)

    router.post("/login", login_handler)
    router.post("/signup", signup_handler)

    router.post("/log/crash_report", crash_report_handler)


    router.post("/auth/hello", initial_greeting_handler)
    router.post("/auth/ack", initial_ack_handler)
    router.post("/auth/challenge/req", signing_challenge_handler)
    router.post("/auth/challenge/res", challenge_submission_handler)


