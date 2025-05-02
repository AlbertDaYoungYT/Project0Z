from dataclasses import dataclass
from enum import Enum
import json

import loguru
from aiohttp import web

from utils.DatabaseAdapter import Serializable


@dataclass(frozen=True)  # Making it frozen as error codes should be immutable
class ErrorDetails(Serializable):
    code: int
    name: str
    message: str

    def to_logger(self, e: Exception | None = None) -> str:
        return f"Error (Code {self.code}) {self.name} '{self.message}'" + str(e.args) if e != None else ""
    
    def to_response(self, e: Exception | None = None, **kwargs):
        return web.json_response(
            self.to_dict(),
            status=self.code,
            **kwargs
        )

class Codes(Enum):
    SUCCESS = ErrorDetails(code=200, name="SUCCESS", message="Operation successful")

    # Authentication Errors (1xx)
    INVALID_CREDENTIALS = ErrorDetails(code=100, name="INVALID_CREDENTIALS", message="Incorrect username or password.")
    ACCOUNT_LOCKED = ErrorDetails(code=101, name="ACCOUNT_LOCKED", message="This account has been temporarily locked.")
    ACCOUNT_BANNED = ErrorDetails(code=102, name="ACCOUNT_BANNED", message="This account has been banned.")
    UNAUTHORIZED_ACCESS = ErrorDetails(code=103, name="UNAUTHORIZED_ACCESS", message="You do not have permission to access this resource.")
    TOKEN_EXPIRED = ErrorDetails(code=104, name="TOKEN_EXPIRED", message="The authentication token has expired.")
    INVALID_TOKEN = ErrorDetails(code=105, name="INVALID_TOKEN", message="The provided authentication token is invalid.")
    SESSION_EXPIRED = ErrorDetails(code=106, name="SESSION_EXPIRED", message="Your session has expired. Please log in again.")
    TOO_MANY_ATTEMPTS = ErrorDetails(code=107, name="TOO_MANY_ATTEMPTS", message="Too many login attempts. Please wait and try again later.")
    MFA_REQUIRED = ErrorDetails(code=108, name="MFA_REQUIRED", message="Multi-factor authentication is required.")
    MFA_FAILED = ErrorDetails(code=109, name="MFA_FAILED", message="Multi-factor authentication failed.")

    CLIENT_VERSION_TOO_LOW = ErrorDetails(code=110, name="CLIENT_VERSION_TOO_LOW", message="The client version does not meet the servers Minimum Requirements.")
    FAILED_LOADING_OFFICIAL_CERTIFICATES = ErrorDetails(code=111, name="FAILED_LOADING_OFFICIAL_CERTIFICATES", message="Failed loading official certificates")
    CLIENT_CHALLENGE_VERIFICATION_FAILED = ErrorDetails(code=112, name="CLIENT_CHALLENGE_VERIFICATION_FAILED", message="Failed to verify Client provided Challenge.")
    CLIENT_INVALID_ID = ErrorDetails(code=113, name="CLIENT_INVALID_ID", message="Client provided ID is invalid.")
    FAILED_GENERATING_AUTH_CHALLENGE = ErrorDetails(code=114, name="FAILED_GENERATING_AUTH_CHALLENGE", message="Server failed to generate or encrypt Authentication Challenge.")
    CLIENT_AUTHENTICATION_TOKEN_INVALID = ErrorDetails(code=115, name="CLIENT_AUTHENTICATION_TOKEN_INVALID", message="Clients Authentication Token is invalid.")


    # User/Account Related Errors (2xx)
    USER_NOT_FOUND = ErrorDetails(code=201, name="USER_NOT_FOUND", message="User with the given identifier not found.")
    USERNAME_TAKEN = ErrorDetails(code=202, name="USERNAME_TAKEN", message="The specified username is already in use.")
    EMAIL_TAKEN = ErrorDetails(code=203, name="EMAIL_TAKEN", message="The specified email address is already registered.")
    INVALID_EMAIL_FORMAT = ErrorDetails(code=204, name="INVALID_EMAIL_FORMAT", message="The provided email address is not in a valid format.")
    PASSWORD_MISMATCH = ErrorDetails(code=205, name="PASSWORD_MISMATCH", message="The provided passwords do not match.")
    ACCOUNT_NOT_VERIFIED = ErrorDetails(code=206, name="ACCOUNT_NOT_VERIFIED", message="This account has not been verified.")
    WEAK_PASSWORD = ErrorDetails(code=207, name="WEAK_PASSWORD", message="The provided password is too weak.")
    PROFILE_INCOMPLETE = ErrorDetails(code=208, name="PROFILE_INCOMPLETE", message="User profile is incomplete.")
    AGE_RESTRICTION = ErrorDetails(code=209, name="AGE_RESTRICTION", message="User does not meet the minimum age requirement.")

    ACCOUNT_CHECK_FAILED = ErrorDetails(code=210, name="ACCOUNT_CHECK_FAILED", message="Account failed to pass checks.")


    # Game Logic Errors (3xx)
    INVALID_GAME_STATE = ErrorDetails(code=300, name="INVALID_GAME_STATE", message="The game is in an invalid state for this action.")
    INVALID_MOVE = ErrorDetails(code=301, name="INVALID_MOVE", message="The attempted move is not valid.")
    INSUFFICIENT_RESOURCES = ErrorDetails(code=302, name="INSUFFICIENT_RESOURCES", message="Not enough resources to perform this action.")
    ITEM_NOT_FOUND = ErrorDetails(code=303, name="ITEM_NOT_FOUND", message="The requested item could not be found.")
    ACTION_NOT_ALLOWED = ErrorDetails(code=304, name="ACTION_NOT_ALLOWED", message="You are not allowed to perform this action at this time.")
    LEVEL_REQUIREMENT_NOT_MET = ErrorDetails(code=305, name="LEVEL_REQUIREMENT_NOT_MET", message="You have not reached the required level.")
    MATCH_NOT_FOUND = ErrorDetails(code=306, name="MATCH_NOT_FOUND", message="The specified match could not be found.")
    ALREADY_IN_PARTY = ErrorDetails(code=307, name="ALREADY_IN_PARTY", message="You are already in a party.")


    # Database Errors (4xx)
    DATABASE_CONNECTION_ERROR = ErrorDetails(code=400, name="DATABASE_CONNECTION_ERROR", message="Failed to connect to the database.")
    DATABASE_QUERY_ERROR = ErrorDetails(code=401, name="DATABASE_QUERY_ERROR", message="An error occurred while executing the database query.")
    DATABASE_RECORD_EXISTS = ErrorDetails(code=402, name="DATABASE_RECORD_EXISTS", message="The record already exists in the database.")
    DATABASE_RECORD_NOT_FOUND = ErrorDetails(code=403, name="DATABASE_RECORD_NOT_FOUND", message="The requested record was not found in the database.")
    DATABASE_TIMEOUT = ErrorDetails(code=404, name="DATABASE_TIMEOUT", message="The database request timed out.")
    TRANSACTION_FAILED = ErrorDetails(code=405, name="TRANSACTION_FAILED", message="The database transaction failed.")
    DUPLICATE_ENTRY = ErrorDetails(code=406, name="DUPLICATE_ENTRY", message="A duplicate entry was found.")
    SCHEMA_MISMATCH = ErrorDetails(code=407, name="SCHEMA_MISMATCH", message="Database schema does not match expected structure.")


    # Input/Validation Errors (5xx)
    MISSING_REQUIRED_FIELD = ErrorDetails(code=500, name="MISSING_REQUIRED_FIELD", message="A required field is missing in the input.")
    INVALID_FIELD_VALUE = ErrorDetails(code=501, name="INVALID_FIELD_VALUE", message="The value provided for a field is invalid.")
    REQUEST_BODY_MALFORMED = ErrorDetails(code=502, name="REQUEST_BODY_MALFORMED", message="The request body is not in the expected format.")
    INVALID_ENUM_VALUE = ErrorDetails(code=503, name="INVALID_ENUM_VALUE", message="An invalid value was provided for an enumerated field.")
    VALUE_OUT_OF_RANGE = ErrorDetails(code=504, name="VALUE_OUT_OF_RANGE", message="A numeric value is outside the allowable range.")
    INVALID_DATE_FORMAT = ErrorDetails(code=505, name="INVALID_DATE_FORMAT", message="The date format is invalid. Expected ISO 8601.")
    UNSUPPORTED_MEDIA_TYPE = ErrorDetails(code=506, name="UNSUPPORTED_MEDIA_TYPE", message="The content type of the request is not supported.")


    # Internal Server Errors (9xx) - Typically unexpected issues
    INTERNAL_SERVER_ERROR = ErrorDetails(code=900, name="INTERNAL_SERVER_ERROR", message="An unexpected internal server error occurred.")
    UNHANDLED_EXCEPTION = ErrorDetails(code=901, name="UNHANDLED_EXCEPTION", message="An unhandled exception was raised.")
    CONFIGURATION_ERROR = ErrorDetails(code=902, name="CONFIGURATION_ERROR", message="There is an issue with the server configuration.")
    SERVICE_UNAVAILABLE = ErrorDetails(code=903, name="SERVICE_UNAVAILABLE", message="The service is currently unavailable.")
    DEPENDENCY_FAILURE = ErrorDetails(code=904, name="DEPENDENCY_FAILURE", message="A required external service failed to respond.")
    MEMORY_OVERLOAD = ErrorDetails(code=905, name="MEMORY_OVERLOAD", message="The server ran out of memory processing the request.")
    RATE_LIMIT_EXCEEDED = ErrorDetails(code=906, name="RATE_LIMIT_EXCEEDED", message="Rate limit exceeded. Slow down your requests.")
    FATAL_SERVER_ERROR = ErrorDetails(code=907, name="FATAL_SERVER_ERROR", message="The server encountered a fatal error.")

