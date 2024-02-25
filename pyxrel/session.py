from typing import Dict, Optional, Literal

import requests

from pyxrel.exceptions import parse_error


class Session(requests.Session):
    """A session for interactions with the xREL.to API."""

    def __init__(
        self,
        host: Optional[Literal["https://api.xrel.to/", "https://xrel-api.nfos.to/"]] = "https://api.xrel.to/",
        **kwargs,
    ) -> None:
        super().__init__()
        self.headers.update(
            {
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; SM-S911B Build/UP1A.231005.007)",
            }
        )

        self.host = host
        self.extra = kwargs

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> requests.Response:
        """Sends an HTTP request to the xREL.to API.

        Handles host prefixing, default headers, and API-specific adjustments.
        """
        if not url.startswith(self.host):
            url = requests.compat.urljoin(self.host, "v2/" + url)

        if headers is None:
            headers = {}

        if method == "POST":
            headers.update(
                {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            )

        headers.update(self.extra.pop("headers", {}))
        kwargs.update(self.extra)

        response = super().request(
            method,
            url,
            headers=headers,
            **kwargs,
        )

        parse_error(response)  # will raise an exception if applicable

        return response
