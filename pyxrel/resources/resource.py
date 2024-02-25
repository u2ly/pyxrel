from abc import ABC
from typing import Optional

from pyxrel.session import Session
from pyxrel.oauth2 import OAuth2


class Resource(ABC):
    """Base class for resources interacting with the xREL API."""

    def __init__(self, session: Optional[Session] = None, oauth2: Optional[OAuth2] = None):
        if not session:
            session = Session()

        self.session = session
        self.oauth2 = oauth2
