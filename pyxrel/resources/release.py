from typing import Optional, Union

from pyxrel.session import Session
from pyxrel.oauth2 import OAuth2
from pyxrel.models import Release as ReleaseScene, ReleaseP2P, Comments
from pyxrel.utils import call, get_rls_type
from pyxrel.resources.resource import Resource
from pyxrel.exceptions import NotFoundError
from pyxrel.types import ReleaseType


class Release(Resource):
    """Interacts with release-related resources on the XREL API."""

    def __init__(self, session: Optional[Session] = None, oauth2: Optional[OAuth2] = None) -> None:
        super().__init__(session, oauth2)

    def __call__(
        self,
        dirname: Optional[str] = None,
        id: Optional[str] = None,
        type: ReleaseType = "scene",
    ) -> Union[ReleaseScene, ReleaseP2P]:
        """Retrieves information about a single release."""
        if dirname is not None and id is not None:
            raise ValueError("Only one of `dirname` or `id` can be provided at a time.")

        if dirname:
            params = {"dirname": dirname}
        elif id:
            params = {"id": id}

        endpoint = "/release/info.json" if type == "scene" else "/p2p/rls_info.json"

        resp = self.session.get(endpoint, params=params).json()

        if type == "scene":
            return ReleaseScene(**resp)

        return ReleaseP2P(**resp)

    def nfo(self, id: str, type: ReleaseType = "scene") -> bytes:
        """Returns an image of a NFO file for a given API release id."""
        return call(
            session=self.session,
            resource=f"/nfo/{get_rls_type(type)}",
            format=False,
            scope="viewnfo",
            oauth2=self.oauth2,
            params={"id": id},
        )

    def comments(self, id: str, type: ReleaseType = "scene", page: int = 1) -> Comments:
        """Returns comments for a given API release id."""
        try:
            return Comments(
                **call(
                    session=self.session,
                    resource="/comments/get",
                    format="json",
                    params={"id": id, "type": get_rls_type(type), "page": page},
                )
            )
        except NotFoundError:
            return Comments(total_count=0, list=[])
