from typing import Optional, List

from pyxrel.models import SearchResult, SearchExtInfo
from pyxrel.resources.resource import Resource
from pyxrel.session import Session
from pyxrel.utils import call
from pyxrel.types import ReleaseType, ExtInfoType


class Search(Resource):
    """Performs search queries for Scene and P2P releases."""

    def __init__(self, session: Optional[Session] = None) -> None:
        super().__init__(session)

    def __call__(self, query: str, limit: int = 25, include: List[ReleaseType] = None) -> SearchResult:
        """Searches for releases based on the provided query and filters."""
        if include is None:
            include = ["scene", "p2p"]
        if not include:
            raise ValueError("At least one of 'scene' or 'p2p' must be included.")

        params = {
            "q": query,
            "scene": 0,
            "p2p": 0,
            "limit": limit,
        }

        params.update({key: 1 for key in include})

        return SearchResult(**call(self.session, "/search/releases", params=params))

    def ext_info(self, query: str, limit: int = 25, type: Optional[ExtInfoType] = None) -> SearchExtInfo:
        """Searches for Ext Info based on the provided query."""
        return SearchExtInfo(
            **call(self.session, "/search/ext_info", params={"q": query, "limit": limit, "type": type})
        )
