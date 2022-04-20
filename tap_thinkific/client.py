"""REST client handling, including thinkificStream base class."""

import requests, datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class thinkificStream(RESTStream):
    """thinkific stream class."""

    url_base = "https://api.thinkific.com/api/public/v1"

    api_date_format = "%Y-%m-%dT%H:%M:%SZ"

    records_jsonpath = "$.items[*]" 

    next_page_token_jsonpath = "$.meta.pagination.next_page"


    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="X-Auth-API-Key",
            value=self.config.get("api_key"),
            location="header"
        )


    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}

        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        
        headers["X-Auth-Subdomain"] = self.config.get("subdomain")

        return headers


    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}

        if next_page_token:
            params["page"] = next_page_token

        return params