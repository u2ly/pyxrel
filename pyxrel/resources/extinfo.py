from typing import Optional

from pyxrel.models import MediaList, ExtInfoInfo, Releases
from pyxrel.resources.resource import Resource
from pyxrel.session import Session
from pyxrel.utils import call


class ExtInfo(Resource):
    """Performs requests for extended information on releases."""

    def __init__(self, session: Optional[Session] = None) -> None:
        super().__init__(session)

    def __call__(self, id: str) -> ExtInfoInfo:
        """Retrieves information about an Ext Info."""
        return ExtInfoInfo(**call(self.session, "/ext_info/info", params={"id": id}))

    def media(self, id: str) -> MediaList:
        """Retrieves media associated with a given Ext Info."""
        return MediaList(list=call(self.session, "/ext_info/media", params={"id": id}))

    def releases(self, id: str, pre_page: int = 25, page: int = 1) -> Releases:
        """Retrieves all releases associated with a given Ext Info."""
        return Releases(
            **call(
                self.session,
                "/release/ext_info",
                params={"id": id, "per_page": pre_page, "page": page},
            )
        )
