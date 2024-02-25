# pyxrel

Python client for the xREL v2 API. Didn't do the user OAuth2 flow yet, cause I personally don't need it (also not sure how). If you need it, feel free to open a PR.

## Installation

```bash
pip install git+https://github.com/u2ly/pyxrel.git
```

## Usage

Return schemas match the [offical xREL API documentation](https://www.xrel.to/wiki/1681/API.html). Changed the method structure slightly to make it more intuitive.

Every method returns a pydantic model for better type hinting. See [pyxrel/models.py](https://github.com/u2ly/pyxrel/blob/main/pyxrel/models.py) for more information.

```python
from pyxrel import XREL

# Fire up the client, optionally with your client credentials
client = XREL(
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Fetch details on a release using its ID or dirname
release = client.release("Wo.die.Luege.hinfaellt.2023.German.DL.HDR.2160p.WEB.h265-W4K", type="scene")

# Retrieve the NFO file, served as bytes
nfo = client.release.nfo(release.id)

# Gather comments linked to the release
comments = client.release.comments(release.id)

# Get information about the title
title = client.ext_info(release.ext_info.id)

# and more...!
```

## License

This project is licensed under the terms of [GNU General Public License, Version 3.0](LICENSE).
