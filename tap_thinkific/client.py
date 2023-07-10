"""REST client handling, including thinkificStream base class."""

import requests, backoff
from pathlib import Path
from typing import Any, Dict, Optional, List, Callable
import logging

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.exceptions import RetriableAPIError

LOGGER = logging.getLogger()

# Log handler
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
LOGGER.addHandler(handler)



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

    def request_decorator(self, func: Callable) -> Callable:

        def backoff_hdlr(details):
            LOGGER.info("Backing off {wait:0.1f} seconds after {tries} tries "
                        "calling function {target} with args {args} and kwargs "
                        "{kwargs}".format(**details))


        # Increase backoff factor and max tries from defaults (2 and 5 respectively)
        decorator: Callable = backoff.on_exception(
            backoff.expo,
            (
                RetriableAPIError,
                requests.exceptions.ReadTimeout,
            ),
            max_tries=16,
            factor=10,
            on_backoff=backoff_hdlr,
        )(func)
        return decorator

    def validate_response(self, response):

        if response.status_code == 429: # 429 == too many requests
            raise RetriableAPIError(response)
        else:
            super().validate_response(response)