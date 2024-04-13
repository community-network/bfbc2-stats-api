import re
from typing import Optional, Any
from urllib.parse import unquote

from fastapi.responses import JSONResponse

from app import config
from app.constants import THEATER_DIRTY_STR_KEYS

NO_INDEX_KEY_REGEX = re.compile(r"^(.*?)(?:\d+)?$")


class CacheableJSONResponse(JSONResponse):
    def __init__(
        self,
        content: Optional[Any] = None,
        headers: Optional[Any] = None,
        max_age: int = config.CACHE_MAX_AGE_DEFAULT,
    ):
        # Set up cache headers
        response_headers = {"Cache-Control": f"public, max-age={max_age}"}
        # Add any given headers
        if isinstance(headers, dict):
            response_headers = {**response_headers, **headers}

        super().__init__(content=content, headers=response_headers)


def clean_string_value(persona_name: str) -> str:
    return unquote(persona_name.replace('"', ""))


def clean_server_details(raw_server: dict) -> dict:
    # Remove pdat entries (which seem to contain encoded player IPs) as well as irrelevant ids
    server = {
        key: value
        for (key, value) in raw_server.items()
        if not key.startswith("D-pdat") and key not in ["TID"]
    }

    # Clean up "dirty" string values
    for key, value in server.items():
        # Some keys contain trailing index indicators (e.g. D-ServerDescription0)
        # => remove index and check if key is in "dirty" list
        non_index_key = NO_INDEX_KEY_REGEX.sub("\\1", key)
        if non_index_key in THEATER_DIRTY_STR_KEYS:
            server[key] = clean_string_value(value)

    # Clean up player list (if present)
    if "D-Players" in server and isinstance(server["D-Players"], list):
        server["D-Players"] = [
            {"pid": int(player["UID"]), "name": clean_string_value(player["NAME"])}
            for player in server["D-Players"]
        ]

    return server
