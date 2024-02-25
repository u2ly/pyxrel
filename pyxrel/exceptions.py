import json
from datetime import datetime

import requests
from lxml import etree as ElementTree

from pyxrel.constants import SCOPES


class XrelToError(Exception):
    """Base class for all xREL.to API errors."""


class AuthenticationError(XrelToError):
    """Base class for authentication-related errors."""


class NotFoundError(XrelToError):
    """Raised when a 404 Not Found error occurs."""


class InternalServerError(XrelToError):
    """Raised when a 500 Internal Server Error occurs."""


class OAuthError(AuthenticationError):
    """Base class for OAuth-related errors."""


class InvalidClientError(OAuthError):
    """Invalid client error."""


class InvalidRequestError(OAuthError):
    """Invalid request error."""


class AccessDeniedError(OAuthError):
    """Access token invalid or expired."""


class UnsupportedGrantTypeError(OAuthError):
    """Unsupported grant type."""


class RequestError(XrelToError):
    """Base class for API request-related errors."""


class InvalidMethodError(RequestError):
    """Wrong HTTP method used."""


class ScopeRequiredError(RequestError):
    """Access token doesn't have the required scope."""


class IDNotFoundError(RequestError):
    """Item with the provided ID was not found."""


class InvalidArgumentError(RequestError):
    """An argument is invalid."""


class UserRequiredError(RequestError):
    """Method requires a user context but used application-based auth."""


class PermissionDeniedError(RequestError):
    """Not enough permissions to perform the action."""


class CommentTooShortError(XrelToError):
    """Comment is too short."""


class CommentTooFastError(XrelToError):
    """Comments are being posted too quickly."""


class ProofNoNewError(XrelToError):
    """All provided releases already have a proof picture."""


class ProofNotSimilarError(XrelToError):
    """The proof picture does not match for the different releases."""


class OutOfBoundsError(XrelToError):
    """Request beyond limits."""


class InternalError(XrelToError):
    """Generic internal error."""


class RateLimitError(XrelToError):
    """Rate limit exceeded."""

    def __init__(self, response: requests.Response) -> None:
        super().__init__(
            "Rate limit exceeded: {remaining} requests remaining. Limit resets at {reset}".format(
                remaining=response.headers["X-RateLimit-Remaining"],
                reset=datetime.fromtimestamp(int(response.headers["X-RateLimit-Reset"])),
            )
        )


class UnknownScopeError(XrelToError):
    """The provided OAuth2 scope is invalid."""

    def __init__(self, scope: str) -> None:
        super().__init__(
            "Invalid OAuth2 scope provided: {scope}. Valid options include: {valid_scopes}".format(
                scope=scope, valid_scopes=", ".join(SCOPES.keys())
            )
        )


class CloudflareError(XrelToError):
    """Raised when a Cloudflare block page is encountered."""

    def __init__(self) -> None:
        super().__init__("Cloudflare blocked the request. Please try again later or use a different IP address.")


def parse_error(response: requests.Response):
    """Parses an error response (if any) and raises the appropriate exception."""

    error_mapping = {
        500: InternalServerError("An internal server error occurred."),
        429: RateLimitError(response) if response.status_code == 429 else None,  # bad code :/ FIXME
        403: CloudflareError if "Just a moment..." in response.text.lower() else None,
        401: NotFoundError("The requested method does not exist.") if "nginx" in response.text.lower() else None,
        404: (
            NotFoundError("The requested resource was not found.")
            if response.headers.get("Content-Type").startswith("text/html")
            else None
        ),
    }

    exception = error_mapping.get(response.status_code)
    if exception:
        raise exception

    content_type = response.headers.get("Content-Type")
    try:
        if content_type.startswith("application/json"):
            try:
                response = response.json()
            except json.decoder.JSONDecodeError:
                # Can't parse the response as JSON even though it's marked as such. This is
                # likely due to a faulty API response at oauth2/token. Already reported to
                # @Doakes on 2024-02-25. So, TODO: remove/ replace after it gets fixed.
                raise XrelToError(f"An unknown error occurred: {response.text}")
        elif content_type.startswith("text/xml"):
            response = {child.tag: child.text for child in ElementTree.fromstring(response.content)}
        else:
            return  # Probably an image + no HTTP error -> no error to raise

        if isinstance(response, dict):
            code = response.get("error")
            message = response.get("error_description")
            if code:
                exc_class = _ERROR_MAP.get(code)
                if exc_class:
                    raise exc_class(message)
                else:
                    raise XrelToError(f"An unknown error occurred: {message}")
    except json.decoder.JSONDecodeError:
        raise XrelToError(f"An unknown error occurred: {response.text}")


_ERROR_MAP = {
    "invalid_client": InvalidClientError,
    "invalid_request": InvalidRequestError,
    "access_denied": AccessDeniedError,
    "unsupported_grant_type": UnsupportedGrantTypeError,
    "invalid_method": InvalidMethodError,
    "scope_required": ScopeRequiredError,
    "id_not_found": IDNotFoundError,
    "invalid_argument": InvalidArgumentError,
    "user_required": UserRequiredError,
    "permission_denied": PermissionDeniedError,
    "comment_too_short": CommentTooShortError,
    "comment_too_fast": CommentTooFastError,
    "proof_no_new": ProofNoNewError,
    "proof_not_similar": ProofNotSimilarError,
    "out_of_bounds": OutOfBoundsError,
    "internal_error": InternalError,
}
