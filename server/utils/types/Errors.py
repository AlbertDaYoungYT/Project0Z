from dataclasses import dataclass
from enum import Enum
import json
from typing import Self

import loguru
from aiohttp import web

from utils.DatabaseAdapter import Serializable

@dataclass
class Error(Serializable):
    code: int
    name: str
    message: str

    http_status: int = 500  # Default to Internal Server Error

    def to_logger(self, e: Exception | None = None) -> str:
        return f"Error (Code {self.code}) {self.name} '{self.message}'" + str(e.args) if e != None else ""

    def to_response(self, e: Exception | None = None, **kwargs):
        return web.json_response(
            self.to_dict(),
            status=self.http_status,
            **kwargs
        )

    @classmethod
    def from_error(cls, other: type[Self]):
        return cls(
            code=other.code,
            name=other.name,
            message=other.message,
            http_status=other.http_status
        )

class Codes(Enum):
    SUCCESS = Error(code=200, name="SUCCESS", message="Operation successful", http_status=200)

    # Authentication Errors (1xx)
    INVALID_CREDENTIALS = Error(code=100, name="INVALID_CREDENTIALS", message="Incorrect username or password.", http_status=401)
    ACCOUNT_LOCKED = Error(code=101, name="ACCOUNT_LOCKED", message="This account has been temporarily locked.", http_status=403)
    ACCOUNT_BANNED = Error(code=102, name="ACCOUNT_BANNED", message="This account has been banned.", http_status=403)
    UNAUTHORIZED_ACCESS = Error(code=103, name="UNAUTHORIZED_ACCESS", message="You do not have permission to access this resource.", http_status=403)
    TOKEN_EXPIRED = Error(code=104, name="TOKEN_EXPIRED", message="The authentication token has expired.", http_status=401)
    INVALID_TOKEN = Error(code=105, name="INVALID_TOKEN", message="The provided authentication token is invalid.", http_status=401)
    SESSION_EXPIRED = Error(code=106, name="SESSION_EXPIRED", message="Your session has expired. Please log in again.", http_status=401)
    TOO_MANY_ATTEMPTS = Error(code=107, name="TOO_MANY_ATTEMPTS", message="Too many login attempts. Please wait and try again later.", http_status=429)
    MFA_REQUIRED = Error(code=108, name="MFA_REQUIRED", message="Multi-factor authentication is required.", http_status=401)
    MFA_FAILED = Error(code=109, name="MFA_FAILED", message="Multi-factor authentication failed.", http_status=401)

    CLIENT_VERSION_TOO_LOW = Error(code=110, name="CLIENT_VERSION_TOO_LOW", message="The client version does not meet the servers Minimum Requirements.", http_status=426)
    FAILED_LOADING_OFFICIAL_CERTIFICATES = Error(code=111, name="FAILED_LOADING_OFFICIAL_CERTIFICATES", message="Failed loading official certificates", http_status=500)
    CLIENT_CHALLENGE_VERIFICATION_FAILED = Error(code=112, name="CLIENT_CHALLENGE_VERIFICATION_FAILED", message="Failed to verify Client provided Challenge.", http_status=401)
    CLIENT_INVALID_ID = Error(code=113, name="CLIENT_INVALID_ID", message="Client provided ID is invalid.", http_status=400)
    FAILED_GENERATING_AUTH_CHALLENGE = Error(code=114, name="FAILED_GENERATING_AUTH_CHALLENGE", message="Server failed to generate or encrypt Authentication Challenge.", http_status=500)
    CLIENT_AUTHENTICATION_TOKEN_INVALID = Error(code=115, name="CLIENT_AUTHENTICATION_TOKEN_INVALID", message="Clients Authentication Token is invalid.", http_status=401)


    # User/Account Related Errors (2xx)
    USER_NOT_FOUND = Error(code=201, name="USER_NOT_FOUND", message="User with the given identifier not found.", http_status=404)
    USERNAME_TAKEN = Error(code=202, name="USERNAME_TAKEN", message="The specified username is already in use.", http_status=409)
    EMAIL_TAKEN = Error(code=203, name="EMAIL_TAKEN", message="The specified email address is already registered.", http_status=409)
    INVALID_EMAIL_FORMAT = Error(code=204, name="INVALID_EMAIL_FORMAT", message="The provided email address is not in a valid format.", http_status=400)
    PASSWORD_MISMATCH = Error(code=205, name="PASSWORD_MISMATCH", message="The provided passwords do not match.", http_status=400)
    ACCOUNT_NOT_VERIFIED = Error(code=206, name="ACCOUNT_NOT_VERIFIED", message="This account has not been verified.", http_status=403)
    WEAK_PASSWORD = Error(code=207, name="WEAK_PASSWORD", message="The provided password is too weak.", http_status=400)
    PROFILE_INCOMPLETE = Error(code=208, name="PROFILE_INCOMPLETE", message="User profile is incomplete.", http_status=400)
    AGE_RESTRICTION = Error(code=209, name="AGE_RESTRICTION", message="User does not meet the minimum age requirement.", http_status=403)

    ACCOUNT_CHECK_FAILED = Error(code=210, name="ACCOUNT_CHECK_FAILED", message="Account failed to pass checks.", http_status=400)


    # Game Logic Errors (3xx)
    INVALID_GAME_STATE = Error(code=300, name="INVALID_GAME_STATE", message="The game is in an invalid state for this action.", http_status=400)
    INVALID_MOVE = Error(code=301, name="INVALID_MOVE", message="The attempted move is not valid.", http_status=400)
    INSUFFICIENT_RESOURCES = Error(code=302, name="INSUFFICIENT_RESOURCES", message="Not enough resources to perform this action.", http_status=402)
    ITEM_NOT_FOUND = Error(code=303, name="ITEM_NOT_FOUND", message="The requested item could not be found.", http_status=404)
    ACTION_NOT_ALLOWED = Error(code=304, name="ACTION_NOT_ALLOWED", message="You are not allowed to perform this action at this time.", http_status=403)
    LEVEL_REQUIREMENT_NOT_MET = Error(code=305, name="LEVEL_REQUIREMENT_NOT_MET", message="You have not reached the required level.", http_status=403)
    MATCH_NOT_FOUND = Error(code=306, name="MATCH_NOT_FOUND", message="The specified match could not be found.", http_status=404)
    ALREADY_IN_PARTY = Error(code=307, name="ALREADY_IN_PARTY", message="You are already in a party.", http_status=409)


    # Database Errors (4xx)
    DATABASE_CONNECTION_ERROR = Error(code=400, name="DATABASE_CONNECTION_ERROR", message="Failed to connect to the database.", http_status=503)
    DATABASE_QUERY_ERROR = Error(code=401, name="DATABASE_QUERY_ERROR", message="An error occurred while executing the database query.", http_status=500)
    DATABASE_RECORD_EXISTS = Error(code=402, name="DATABASE_RECORD_EXISTS", message="The record already exists in the database.", http_status=409)
    DATABASE_RECORD_NOT_FOUND = Error(code=403, name="DATABASE_RECORD_NOT_FOUND", message="The requested record was not found in the database.", http_status=404)
    DATABASE_TIMEOUT = Error(code=404, name="DATABASE_TIMEOUT", message="The database request timed out.", http_status=504)
    TRANSACTION_FAILED = Error(code=405, name="TRANSACTION_FAILED", message="The database transaction failed.", http_status=500)
    DUPLICATE_ENTRY = Error(code=406, name="DUPLICATE_ENTRY", message="A duplicate entry was found.", http_status=409)
    SCHEMA_MISMATCH = Error(code=407, name="SCHEMA_MISMATCH", message="Database schema does not match expected structure.", http_status=500)


    # Input/Validation Errors (5xx)
    MISSING_REQUIRED_FIELD = Error(code=500, name="MISSING_REQUIRED_FIELD", message="A required field is missing in the input.", http_status=400)
    INVALID_FIELD_VALUE = Error(code=501, name="INVALID_FIELD_VALUE", message="The value provided for a field is invalid.", http_status=400)
    REQUEST_BODY_MALFORMED = Error(code=502, name="REQUEST_BODY_MALFORMED", message="The request body is not in the expected format.", http_status=400)
    INVALID_ENUM_VALUE = Error(code=503, name="INVALID_ENUM_VALUE", message="An invalid value was provided for an enumerated field.", http_status=400)
    VALUE_OUT_OF_RANGE = Error(code=504, name="VALUE_OUT_OF_RANGE", message="A numeric value is outside the allowable range.", http_status=400)
    INVALID_DATE_FORMAT = Error(code=505, name="INVALID_DATE_FORMAT", message="The date format is invalid. Expected ISO 8601.", http_status=400)
    UNSUPPORTED_MEDIA_TYPE = Error(code=506, name="UNSUPPORTED_MEDIA_TYPE", message="The content type of the request is not supported.", http_status=415)


    # Internal Server Errors (9xx) - Typically unexpected issues
    INTERNAL_SERVER_ERROR = Error(code=900, name="INTERNAL_SERVER_ERROR", message="An unexpected internal server error occurred.", http_status=500)
    UNHANDLED_EXCEPTION = Error(code=901, name="UNHANDLED_EXCEPTION", message="An unhandled exception was raised.", http_status=500)
    CONFIGURATION_ERROR = Error(code=902, name="CONFIGURATION_ERROR", message="There is an issue with the server configuration.", http_status=500)
    SERVICE_UNAVAILABLE = Error(code=903, name="SERVICE_UNAVAILABLE", message="The service is currently unavailable.", http_status=503)
    DEPENDENCY_FAILURE = Error(code=904, name="DEPENDENCY_FAILURE", message="A required external service failed to respond.", http_status=502)
    MEMORY_OVERLOAD = Error(code=905, name="MEMORY_OVERLOAD", message="The server ran out of memory processing the request.", http_status=500)
    RATE_LIMIT_EXCEEDED = Error(code=906, name="RATE_LIMIT_EXCEEDED", message="Rate limit exceeded. Slow down your requests.", http_status=429)
    FATAL_SERVER_ERROR = Error(code=907, name="FATAL_SERVER_ERROR", message="The server encountered a fatal error.", http_status=500)
    INDEX_ERROR = Error(code=908, name="INDEX_ERROR", message="The server ran into an Index Error.", http_status=500)


    # (10xx) - Critical warnings or errors
    DIRECTORY_EXISTS = Error(code=1000, name="DIRECTORY_EXISTS", message="The Directory or File already exists.", http_status=500)
    FILE_NOT_FOUND = Error(code=1001, name="FILE_NOT_FOUND", message="The File was not found.", http_status=500)