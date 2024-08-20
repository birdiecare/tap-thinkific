"""REST client handling, including ThinkificStream base class."""

from __future__ import annotations

import sys, logging, backoff, requests
from typing import TYPE_CHECKING, Any, Callable

from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.exceptions import RetriableAPIError
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.helpers.types import Context
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

LOGGER = logging.getLogger()

# Log handler
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
LOGGER.addHandler(handler)

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class ThinkificStream(RESTStream):
    """Thinkific stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.thinkific.com/api/public/v1"

    @property
    def api_date_format(self) -> str:
        """Return the date format string for the API."""
        return "%Y-%m-%dT%H:%M:%SZ"

    @property
    def records_jsonpath(self) -> str:
        """Return the JSON path to the records, or None if a root records list."""
        return "$.items[*]"

    @property
    def next_page_token_jsonpath(self) -> str:
        """Return the JSON path to the next page token, or None if no pagination."""
        return "$.meta.pagination.next_page"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="X-Auth-API-Key",
            value=self.config.get("api_key", ""),
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        headers["User-Agent"] = "Meltano Tap for Thinkific: https://hub.meltano.com/extractors/tap-thinkific/"
        headers["X-Auth-Subdomain"] = self.config.get("subdomain")
        return headers

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
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