from typing import Optional

from pyxrel.session import Session
from pyxrel.models import Upcoming
from pyxrel.resources.resource import Resource
from pyxrel.utils import call


class Calendar(Resource):
    """Fetches upcoming movies and their releases from the xREL API."""

    def __init__(self, session: Optional[Session] = None) -> None:
        super().__init__(session)

    def upcoming(self, country: str = "de") -> Upcoming:
        """Retrieves a list of upcoming movies for a specific country."""
        response = call(self.session, "/calendar/upcoming", params={"country": country})
        return Upcoming(list=response)
