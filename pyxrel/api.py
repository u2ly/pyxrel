from typing import Optional, Union, Literal
from lxml import etree as ElementTree

from pyxrel.session import Session
from pyxrel.oauth2 import OAuth2
from pyxrel.resources import Calendar, Release, Search, ExtInfo
from pyxrel.utils import get_rls_type, call as _call
from pyxrel.models import Categories, CategoriesP2P, Releases, ReleasesP2P, Filters
from pyxrel.types import ExtInfoType, ReleaseType


class XREL:
    """Client for interacting with the xREL.to API."""

    def __init__(
        self,
        host: str = "https://api.xrel.to/",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        **request_kwargs,  # Keyword arguments for requests.Session.request
    ) -> None:
        self.session = Session(host, **request_kwargs)
        self.oauth2 = OAuth2(client_id, client_secret, self.session) if client_id and client_secret else None

        self.calendar = Calendar(self.session)
        self.ext_info = ExtInfo(self.session)
        self.release = Release(self.session, self.oauth2)
        self.search = Search(self.session)

    def latest(
        self, archive: Optional[str] = None, per_page: int = 25, page: int = 1, filter: Optional[str] = None
    ) -> Releases:
        """Retrieves the latest releases from the xREL API."""
        return Releases(
            **self.call(
                "/release/latest",
                params={
                    "archive": archive,
                    "per_page": per_page,
                    "page": page,
                    "filter": filter,
                },
            )
        )

    def scene_releases(
        self,
        per_page: int = 25,
        page: int = 1,
        category_name: Optional[str] = None,
        ext_info_type: Optional[ExtInfoType] = None,
    ) -> Releases:
        """Retrieves scene releases based on the provided filters."""
        return Releases(
            **self.call(
                "release/browse_category",
                params={
                    "per_page": per_page,
                    "page": page,
                    "category_name": category_name,
                    "ext_info_type": ext_info_type,
                },
            )
        )

    def p2p_releases(
        self,
        per_page: int = 25,
        page: int = 1,
        category_id: Optional[str] = None,
        group_id: Optional[str] = None,
        ext_info_id: Optional[str] = None,
    ) -> ReleasesP2P:
        """Retrieve P2P/non-scene releases.

        You can optionally filter the list by providing 'one' of the following params:

        * `category_id`: P2P category ID from p2p/categories
        * `group_id`: P2P release group ID
        * `ext_info_id`: Ext Info ID

        Only one of these filtering parameters can be provided at a time.
        """
        if sum(arg is not None for arg in (category_id, group_id, ext_info_id)) > 1:
            raise ValueError("Only one of 'category_id', 'group_id', or 'ext_info_id' can be provided at a time.")

        return ReleasesP2P(
            **self.call(
                "/p2p/releases",
                params={
                    "per_page": per_page,
                    "page": page,
                    "category_id": category_id,
                    "group_id": group_id,
                    "ext_info_id": ext_info_id,
                },
            )
        )

    def categories(self, type: ReleaseType = "scene") -> Union[Categories, CategoriesP2P]:
        """Retrieves a list of release categories."""
        response = self.call(f"/{get_rls_type(type, True)}/categories")
        return Categories(list=response) if type == "scene" else CategoriesP2P(list=response)

    def filters(self) -> Filters:
        """Retrieves a list of filters for the search endpoint."""
        return Filters(filters=self.call("release/filters"))

    def call(
        self,
        resource: str,
        format: Optional[Union[str, Literal[False]]] = "json",
        scope: Optional[str] = None,
        **kwargs,
    ) -> Union[dict, ElementTree.Element, bytes]:
        """Makes a request to the xREL.to API."""
        return _call(self.session, resource, format, scope, self.oauth2, **kwargs)
