"""thinkific tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_thinkific.streams import (
    CoursesStream,
    EnrollmentsStream,
    thinkificStream
)

STREAM_TYPES = [
    CoursesStream,
    EnrollmentsStream
]


class Tapthinkific(Tap):
    """thinkific tap class."""
    name = "tap-thinkific"

    config_jsonschema = th.PropertiesList(

        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="Thinkific API key. See https://developers.thinkific.com/api/api-key-auth."
        ),
        th.Property(
            "subdomain",
            th.StringType,
            required=True,
            description="Subdomain of the Thinkific site. See https://developers.thinkific.com/api/api-key-auth."
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Only sync records updated after this date."
        )
        
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
