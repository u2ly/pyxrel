import time
from typing import Optional

from pyxrel.constants import SCOPES
from pyxrel.exceptions import UnknownScopeError
from pyxrel.session import Session


class OAuth2:
    """Manages OAuth2 authentication and access tokens."""

    _cache = {}

    def __init__(self, client_id: str, client_secret: str, session: Optional[Session] = None, **kwargs) -> None:
        if not client_id:
            raise ValueError("Client ID must be provided.")
        if not isinstance(client_id, str):
            raise TypeError(f"Expected Client ID to be a string, not {client_id!r}.")

        if not client_secret:
            raise ValueError("Client secret must be provided.")
        if not isinstance(client_secret, str):
            raise TypeError(f"Expected Client secret to be a string, not {client_secret!r}.")

        self.client_id = client_id
        self.client_secret = client_secret

        self.session = session or Session(**kwargs)

    def get_access_token(self, scope: str) -> str:
        """Retrieves an access token for the given scope."""
        if scope not in SCOPES:
            raise UnknownScopeError(scope)

        cache_key = f"{self.client_id}:{self.client_secret}:{scope}"

        data = self._cache.get(cache_key)
        if data and not self._is_expired(data):
            return data["access_token"]

        data = self.session.post(
            "oauth2/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
                "scope": scope,
            },
        ).json()

        self._cache[cache_key] = {
            "access_token": data["access_token"],
            "expires_at": time.time() + data["expires_in"],
        }

        return data["access_token"]

    @staticmethod
    def _is_expired(data: dict) -> bool:
        """Checks if the access token has expired."""
        return data["expires_at"] < time.time()
