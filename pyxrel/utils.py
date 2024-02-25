from typing import Optional, Union
from lxml import etree as ElementTree

from pyxrel.session import Session
from pyxrel.oauth2 import OAuth2
from pyxrel.constants import TYPE_MAP


def get_rls_type(type: str, short: bool = False) -> str:
    """Returns the API type based on the given type."""
    type = TYPE_MAP.get(type)

    if short:
        return type.split("_")[0]

    return type


def call(
    session: Session,
    resource: str,
    format: Optional[str] = "json",
    scope: Optional[str] = None,
    oauth2: OAuth2 = None,
    **kwargs,
) -> Union[dict, ElementTree.Element, bytes]:
    """Makes a request to the xREL.to API."""
    if scope:
        if not oauth2:
            raise ValueError("No OAuth2 instance provided.")

        kwargs["headers"] = {
            **kwargs.get("headers", {}),
            "Authorization": f"Bearer {oauth2.get_access_token(scope)}",
        }

    resource += (
        f".{format}" if format else ".json"
    )  # Errors will be JSON even if the successful response is another format, kinda dirty. TODO: fix this

    resp = session.get(resource, **kwargs)

    if format == "json":
        return resp.json()
    if format == "xml":
        return ElementTree.fromstring(resp.content)

    return resp.content
