from .api import XREL
from .oauth2 import OAuth2
from .session import Session


def new(host: str = "https://api.xrel.to/", client_id: str = None, client_secret: str = None, **request_kwargs):
    """Creates a new xREL client."""
    return XREL(host, client_id, client_secret, **request_kwargs)


__all__ = ("XREL", "OAuth2", "Session")
